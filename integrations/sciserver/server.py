"""Read-only SciServer MCP v0.1.1 interface with bounded HTTP requests."""

import json
import os
import stat
import time
from pathlib import Path

import pandas as pd
import requests
from mcp.server.fastmcp import FastMCP
from SciServer import Authentication, Config

if __package__:
    from .identifiers import exact_objid
else:
    from identifiers import exact_objid

mcp = FastMCP("star-sciserver")
TOKEN_FILE = Path.home() / ".config" / "star-sciserver" / "token"
DR18_CONTEXT = "DR18"
MYDB_CONTEXT = "MyDB"
CONNECT_TIMEOUT_SECONDS = 5
READ_TIMEOUT_SECONDS = 5
OVERALL_DEADLINE_SECONDS = 30
MAX_RESPONSE_BYTES = 2 * 1024 * 1024
TASK_NAME = "STAR-Labs.SciServer.MCP.readonly"


def authenticate() -> str:
    """Load a token from one validated, non-symlink POSIX file descriptor.

    Native Windows ACL validation is not implemented; Windows users must use
    WSL2. Never silently skip token ownership and permission validation.
    """
    if os.name != "posix" or not hasattr(os, "O_NOFOLLOW") or not hasattr(os, "getuid"):
        raise RuntimeError(
            "Secure SciServer token authentication requires POSIX/WSL2; "
            "native Windows is unsupported"
        )

    flags = os.O_RDONLY | os.O_NOFOLLOW | getattr(os, "O_CLOEXEC", 0)
    # Avoid blocking on a replacement FIFO; fstat below rejects non-regular files.
    flags |= getattr(os, "O_NONBLOCK", 0)
    fd = os.open(TOKEN_FILE, flags)
    try:
        info = os.fstat(fd)
        if not stat.S_ISREG(info.st_mode):
            raise PermissionError("SciServer token must be a regular file")
        if info.st_uid != os.getuid():
            raise PermissionError("SciServer token ownership is invalid")
        if stat.S_IMODE(info.st_mode) & 0o077:
            raise PermissionError(
                "SciServer token permissions must be 0600 or more restrictive"
            )
        if info.st_size > 4096:
            raise ValueError("SciServer token file exceeds size limit")
        with os.fdopen(fd, "r", encoding="utf-8") as stream:
            fd = -1  # stream now owns the descriptor
            token = stream.read(4097).strip()
        if not token or len(token) > 4096:
            raise ValueError("SciServer token file is empty or exceeds size limit")
        Authentication.token.value = token
        return token
    finally:
        if fd >= 0:
            os.close(fd)


DR18_SMOKE_SQL = """
SELECT TOP 10
    CAST(p.objid AS VARCHAR(20)) AS objid,
    p.ra,
    p.dec,
    p.u,
    p.g,
    p.r
FROM PhotoObj AS p
ORDER BY p.objid ASC
"""


def _read_json(method: str, context: str, token: str, sql: str | None = None) -> object:
    """Use only the two approved read-only CasJobs REST routes.

    SciServer 2.2.0's SDK methods omit request timeouts, so this narrow adapter
    uses requests connect/read timeouts, a size cap, and a streaming deadline.
    The deadline is checked between reads; it does not cancel remote SQL.
    """
    base = Config.CasJobsRESTUri.rstrip("/")
    if not base.startswith("https://"):
        raise RuntimeError("SciServer CasJobs REST endpoint must use HTTPS")
    if method == "POST" and context == DR18_CONTEXT and sql == DR18_SMOKE_SQL:
        url = base + "/contexts/DR18/query"
        headers = {"X-Auth-Token": token, "Accept": "application/json+array"}
        send = lambda: requests.post(
            url,
            params={"TaskName": TASK_NAME},
            json={"Query": sql, "TaskName": TASK_NAME},
            headers=headers,
            timeout=(CONNECT_TIMEOUT_SECONDS, READ_TIMEOUT_SECONDS),
            stream=True,
            allow_redirects=False,
        )
    elif method == "GET" and context == MYDB_CONTEXT and sql is None:
        url = base + "/contexts/MyDB/Tables"
        headers = {"X-Auth-Token": token, "Accept": "application/json"}
        send = lambda: requests.get(
            url,
            params={"TaskName": TASK_NAME},
            headers=headers,
            timeout=(CONNECT_TIMEOUT_SECONDS, READ_TIMEOUT_SECONDS),
            stream=True,
            allow_redirects=False,
        )
    else:
        raise ValueError("Unapproved SciServer request")

    started = time.monotonic()
    try:
        with send() as response:
            if response.status_code != 200:
                raise RuntimeError(f"SciServer returned HTTP {response.status_code}")
            chunks = []
            count = 0
            for chunk in response.iter_content(chunk_size=65536):
                if time.monotonic() - started > OVERALL_DEADLINE_SECONDS:
                    raise TimeoutError("SciServer response deadline exceeded")
                count += len(chunk)
                if count > MAX_RESPONSE_BYTES:
                    raise ValueError("SciServer response exceeds configured size limit")
                chunks.append(chunk)
            return json.loads(b"".join(chunks))
    except requests.RequestException:
        raise RuntimeError("SciServer network request failed or timed out") from None


@mcp.tool()
def dr18_smoke_test() -> dict:
    """Execute the fixed, read-only DR18 smoke query."""
    token = authenticate()
    payload = _read_json("POST", DR18_CONTEXT, token, DR18_SMOKE_SQL)
    if not isinstance(payload, dict) or not isinstance(payload.get("Result"), list):
        raise ValueError("Unexpected SciServer query response")
    results = payload["Result"]
    if len(results) != 1 or not isinstance(results[0], dict):
        raise ValueError("Expected exactly one SciServer result set")
    result = results[0]
    df = pd.DataFrame(result["Data"], columns=result["Columns"])
    if "objid" not in df.columns:
        raise RuntimeError("SciServer response does not contain objid")
    first_objid = exact_objid(df["objid"].iat[0]) if not df.empty else None
    return {
        "context": DR18_CONTEXT,
        "row_count": int(len(df)),
        "columns": [str(c) for c in df.columns],
        "first_objid": first_objid,
        "identifier_integrity": "exact_decimal",
        "read_only": True,
    }


@mcp.tool()
def list_mydb_tables() -> list[dict]:
    """Return MyDB table metadata without modifying the database."""
    token = authenticate()
    tables = _read_json("GET", MYDB_CONTEXT, token)
    if not isinstance(tables, list) or any(not isinstance(t, dict) for t in tables):
        raise TypeError("Unexpected MyDB table response format")
    return tables


if __name__ == "__main__":
    mcp.run(transport="stdio")
