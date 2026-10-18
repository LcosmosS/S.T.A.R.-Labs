# SciServer MCP v0.1.1 — bounded read-only integration

The two MCP tools are `dr18_smoke_test` (fixed DR18 query) and
`list_mydb_tables` (metadata only). Neither writes to MyDB or changes
scientific registries. No arbitrary SQL is accepted.

Install optional runtime dependencies from the repository root:

```bash
python -m pip install -e '.[sciserver]'
```

Token: `~/.config/star-sciserver/token`, owned by the current WSL/POSIX
user with mode `0600` (or stricter), stored outside Git. The token is opened
once with `O_NOFOLLOW`; type, UID and mode are checked by `fstat` before
reading the same descriptor. Native Windows authentication is **not supported**;
use WSL2. This avoids treating Windows mode bits as a substitute for ACL checks.

SciServer 2.2.0 does not expose timeout parameters for `CasJobs.executeQuery`
and `CasJobs.getTables`. The two fixed read-only REST routes are therefore
called through `requests` with 5-second connect/read timeouts, a 30-second
streaming deadline, and a 2-MiB response limit. The streaming deadline is
checked at read boundaries; it does not cancel a server-side query and should
not be presented as a hard real-time deadline.

The DR18 query casts `objid` to character data and the response accesses
`df["objid"].iat[0]` to avoid mixed-row floating-point coercion.

Unit tests mock MCP, SciServer, and network traffic; no live credentials are
needed for CI. This release performs no asynchronous CasJobs submission.
