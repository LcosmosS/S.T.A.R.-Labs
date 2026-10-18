"""Offline regression tests of the production SciServer MCP tools."""

import importlib.util
import os
import sys
import types
from pathlib import Path

import pytest

SERVER = Path(__file__).resolve().parents[2] / "integrations/sciserver/server.py"
EXPECTED = "1237645876861272071"


@pytest.fixture
def server(monkeypatch):
    """Import the production module with fake optional SDK/MCP modules."""
    mcp = types.ModuleType("mcp")
    mcp_server = types.ModuleType("mcp.server")
    mcp_fast = types.ModuleType("mcp.server.fastmcp")

    class FastMCP:
        def __init__(self, name):
            self.name = name

        def tool(self):
            return lambda fn: fn

    mcp_fast.FastMCP = FastMCP
    sciserver = types.ModuleType("SciServer")
    sciserver.Authentication = types.SimpleNamespace(
        token=types.SimpleNamespace(value=None)
    )
    sciserver.Config = types.SimpleNamespace(
        CasJobsRESTUri="https://sciserver.invalid/CasJobsRestApi"
    )
    for name, module in {
        "mcp": mcp,
        "mcp.server": mcp_server,
        "mcp.server.fastmcp": mcp_fast,
        "SciServer": sciserver,
    }.items():
        monkeypatch.setitem(sys.modules, name, module)
    spec = importlib.util.spec_from_file_location(
        "integrations.sciserver._test_server", SERVER
    )
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_production_smoke_preserves_identifier_in_mixed_numeric_row(server, monkeypatch):
    """This fails if production uses df.iloc[0]['objid'] mixed-row coercion."""
    monkeypatch.setattr(server, "authenticate", lambda: "fake")
    monkeypatch.setattr(
        server, "_read_json", lambda *args: {
            "Result": [{
                "Columns": ["objid", "ra", "dec", "u", "g", "r"],
                "Data": [[1237645876861272071, 336.439637, -0.837205,
                          16.9, 14.36237, 13.8]],
            }]
        }
    )
    result = server.dr18_smoke_test()
    assert result["first_objid"] == EXPECTED
    assert result["identifier_integrity"] == "exact_decimal"
    assert result["row_count"] == 1


def test_mydb_tables_mcp_read_only_response(server, monkeypatch):
    monkeypatch.setattr(server, "authenticate", lambda: "fake")
    monkeypatch.setattr(
        server, "_read_json", lambda *args: [{"Name": "MyTable_0", "Rows": 10}]
    )
    assert server.list_mydb_tables()[0]["Rows"] == 10


def test_secure_token_fd_survives_path_replacement(server, monkeypatch, tmp_path):
    original = tmp_path / "token"
    original.write_text("legitimate", encoding="utf-8")
    original.chmod(0o600)
    monkeypatch.setattr(server, "TOKEN_FILE", original)
    real_open = os.open

    def swap_after_open(path, flags, *args, **kwargs):
        fd = real_open(path, flags, *args, **kwargs)
        original.rename(tmp_path / "saved-token")
        original.write_text("attacker", encoding="utf-8")
        original.chmod(0o666)
        return fd

    monkeypatch.setattr(server.os, "open", swap_after_open)
    assert server.authenticate() == "legitimate"
    assert server.Authentication.token.value == "legitimate"


def test_secure_token_rejects_symlink(server, monkeypatch, tmp_path):
    path = tmp_path / "token"
    target = tmp_path / "other"
    target.write_text("attack")
    target.chmod(0o600)
    path.symlink_to(target)
    monkeypatch.setattr(server, "TOKEN_FILE", path)
    with pytest.raises(OSError):
        server.authenticate()


def test_secure_token_rejects_insecure_mode(server, monkeypatch, tmp_path):
    path = tmp_path / "token"
    path.write_text("attack")
    path.chmod(0o644)
    monkeypatch.setattr(server, "TOKEN_FILE", path)
    with pytest.raises(PermissionError):
        server.authenticate()


def test_secure_token_rejects_missing_posix_primitives(server, monkeypatch):
    monkeypatch.delattr(server.os, "getuid")
    with pytest.raises(RuntimeError, match="POSIX/WSL2"):
        server.authenticate()


def test_http_timeout_options_and_transport(server, monkeypatch):
    seen = {}
    payload = b'{"Result":[{"Columns":["objid"],"Data":[["1237645876861272071"]]}]}'

    class Response:
        status_code = 200

        def __enter__(self):
            return self

        def __exit__(self, *args):
            pass

        def iter_content(self, chunk_size):
            return iter([payload])

    def post(url, **kwargs):
        seen.update(url=url, **kwargs)
        return Response()

    monkeypatch.setattr(server.requests, "post", post)
    result = server._read_json(
        "POST", server.DR18_CONTEXT, "opaque", server.DR18_SMOKE_SQL
    )
    assert result["Result"][0]["Data"][0][0] == EXPECTED
    assert seen["timeout"] == (5, 5)
    assert seen["allow_redirects"] is False
    assert seen["stream"] is True
    assert seen["headers"]["X-Auth-Token"] == "opaque"


def test_http_rejects_unsafe_context(server):
    with pytest.raises(ValueError):
        server._read_json("POST", "MyDB", "fake", "DROP TABLE X")


def test_http_declared_deadline(server, monkeypatch):
    class Response:
        status_code = 200

        def __enter__(self):
            return self

        def __exit__(self, *args):
            pass

        def iter_content(self, chunk_size):
            return iter([b"{}"])

    monkeypatch.setattr(server.requests, "get", lambda *a, **kw: Response())
    calls = iter([0, 31])
    monkeypatch.setattr(server.time, "monotonic", lambda: next(calls))
    with pytest.raises(TimeoutError):
        server._read_json("GET", server.MYDB_CONTEXT, "fake")
