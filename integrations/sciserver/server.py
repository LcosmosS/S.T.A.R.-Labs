

"""
S.T.A.R.-Labs — SciServer MCP Integration
Version: 0.1.1

Read-only interface to SciServer CasJobs.

Capabilities:
    - Fixed SDSS DR18 smoke test
    - Read-only MyDB table enumeration

Security:
    - Token stored outside the Git repository
    - Token ownership and permissions validated
    - No credentials written to stdout
    - No arbitrary SQL execution
    - No database write operations

Scientific integrity:
    - Preserve exact SDSS object identifiers
    - Reject floating-point identifiers
    - Return identifiers as decimal strings
"""

import os
import stat
from pathlib import Path

from mcp.server.fastmcp import FastMCP
from SciServer import Authentication, CasJobs

if __package__:
    from .identifiers import exact_objid
else:
    from identifiers import exact_objid


# ============================================================
# MCP INITIALIZATION
# ============================================================

mcp = FastMCP("star-sciserver")

TOKEN_FILE = (
    Path.home()
    / ".config"
    / "star-sciserver"
    / "token"
)

DR18_CONTEXT = "DR18"
MYDB_CONTEXT = "MyDB"


# ============================================================
# AUTHENTICATION
# ============================================================

def authenticate() -> None:
    """
    Load an existing SciServer authentication token.

    The token must:
        - Exist as a regular file
        - Not be a symbolic link
        - Belong to the current user
        - Have no group or other permissions

    Authentication is noninteractive.
    Credentials are never printed.
    """

    if TOKEN_FILE.is_symlink():
        raise PermissionError(
            "SciServer token must not be a symbolic link."
        )

    info = TOKEN_FILE.stat()

    if not stat.S_ISREG(info.st_mode):
        raise PermissionError(
            "SciServer token must be a regular file."
        )

    if info.st_uid != os.getuid():
        raise PermissionError(
            "SciServer token ownership is invalid."
        )

    if stat.S_IMODE(info.st_mode) & 0o077:
        raise PermissionError(
            "SciServer token permissions are insecure. "
            "Expected mode 600 or more restrictive."
        )

    token = TOKEN_FILE.read_text(
        encoding="utf-8"
    ).strip()

    if not token:
        raise RuntimeError(
            "SciServer authentication token is empty."
        )

    # SciServer SDK authentication mechanism.
    # Never print or include this value in MCP output.
    Authentication.token.value = token


# ============================================================
# FIXED DR18 READ-ONLY QUERY
# ============================================================

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


@mcp.tool()
def dr18_smoke_test() -> dict:
    """
    Execute a fixed, read-only SDSS DR18 query.

    Returns:
        - Database context
        - Row count
        - Column names
        - Exact first SDSS object identifier

    The query is fixed and cannot be replaced by tool callers.
    """

    authenticate()

    df = CasJobs.executeQuery(
        sql=DR18_SMOKE_SQL,
        context=DR18_CONTEXT,
        format="pandas",
    )

    if "objid" not in df.columns:
        raise RuntimeError(
            "SciServer response does not contain objid."
        )

    first_objid = None

    if not df.empty:
        # CRITICAL:
        # Access the column directly.
        # Do not use df.iloc[0]["objid"], which can
        # convert integers to floating-point values.

        raw_objid = df["objid"].iat[0]

        first_objid = exact_objid(raw_objid)

    return {
        "context": DR18_CONTEXT,
        "row_count": int(len(df)),
        "columns": [str(c) for c in df.columns],
        "first_objid": first_objid,
        "identifier_integrity": "exact_decimal",
        "read_only": True,
    }


# ============================================================
# MYDB TABLE ENUMERATION
# ============================================================

@mcp.tool()
def list_mydb_tables() -> list[dict]:
    """
    Retrieve metadata for tables in the user's MyDB.

    Read-only operation.
    Does not execute SQL or modify database objects.
    """

    authenticate()

    tables = CasJobs.getTables(MYDB_CONTEXT)

    if not isinstance(tables, list):
        raise TypeError(
            "Unexpected MyDB table response format."
        )

    return tables


# ============================================================
# MCP ENTRY POINT
# ============================================================

if __name__ == "__main__":
    mcp.run(transport="stdio")
