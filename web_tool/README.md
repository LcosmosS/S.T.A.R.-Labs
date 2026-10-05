# STARMAP by S.T.A.R. Labs

A working exploratory prototype: interactive arithmetic projection, searchable
illustrative catalog, RTCH toy dynamics, educational topology/rank diagnostics,
the repository's read-only registry, and a public demo notebook.

## Evidence boundary

The browser catalog contains 12 handwritten illustrative records and 148 seeded
synthetic records. These are not verified LMFDB exports. Synthetic features depend
on rank; omitting rank as a coordinate does not establish independence. Browser
diagnostics are educational, not `EXP-MAP-A01` execution or scientific evidence.

`/registry` is generated from canonical repository files, with their SHA-256 hashes
and the controlled spec's binding checks. It displays declared gates without
editing them or granting execution. Run `npm run registry:sync` after intentional
canonical source changes; `npm run registry:check` rejects a stale snapshot.

## Development and verification

Use Node 24 and npm. From `web_tool`, run `npm ci`, `npm test`, `npm run build`, and
`npm run typecheck`. After deployment linkage and environment verification,
`npm run dev` starts the app. `startup.sh` supports Linux hosts from its own
directory. `npm run preview` serves the built app on port 8081 for verification.

Without a database, local notebook rows live in an in-memory PGLite instance and
reset when the server stops; the UI labels this explicitly. On Vercel, notebook
endpoints return 503 when `DATABASE_URL` is absent instead of accepting ephemeral
saves. The rest of the illustrative lab remains usable.

Run `node scripts/browser-smoke.mjs http://127.0.0.1:8081/ screenshots/built.png`
to inspect desktop/mobile rendering and console errors. Review both PNGs. The
Linux preview process helper `preview:restart` remains available for the original
host; on Windows run `npm run preview` directly.

## Neon and Vercel launch

1. Link this repository to the chosen Vercel account with root directory
   `web_tool`, Node 24, install command `npm ci`, and build command `npm run build`.
   Deploy the verified prototype branch before considering a merge.
   Automatic Git deployments are limited to `main` and `prototype/starmap` by
   `vercel.json`. Set the project's Ignored Build Step to
   `case "$VERCEL_GIT_COMMIT_REF" in main|prototype/starmap) exit 1 ;; *) exit 0 ;; esac`
   as well: scientific branches that predate this configuration must also be
   excluded. Add any future deployment branch deliberately to both rules.
   Vercel skips are deployment
   routing decisions; preregistration validity is established by S.T.A.R. CI.
2. In the existing Neon project, create a dedicated STARMAP prototype branch.
   Use its pooled connection for server-only `DATABASE_URL` and its direct
   connection for local-only `DATABASE_URL_UNPOOLED`. Keep credentials out of Git and logs.
   Isolate preview branches from any production database.
3. Grant a dedicated runtime role only SELECT/INSERT on `starmap_demo_snapshots`
   and SELECT/INSERT/UPDATE on `starmap_demo_budget`, plus schema USAGE.
   Use this role's pooled URL as Vercel's encrypted `DATABASE_URL`; keep the
   migration owner's direct URL local. Configure only the intended environments and
   verify linkage before database changes. Auth is deliberately off; this app
   stores no profiles or private research. `.grok/app-env.json` supplies
   `VITE_AUTH_ENABLED=false`; an explicit provider override must match.
4. Run `npm run db:migrate` once with the intended branch's credentials supplied
   securely to the process. Migrations are explicit, not a side effect of builds.
   Only top-level `migrations/*.sql` apply; opt-in auth SQL is excluded.
5. Deploy a preview, verify `/api/health` reports `storage: neon` and
   `durable: true` (including both schema readiness checks), then save, open a share link in a fresh browser session,
   restore settings and export JSON. Promote only the verified deployment.

Public snapshots are append-only, contain only bounded demo settings, and are
deduplicated by a SHA-256 digest of their version and canonical settings. There
are no update/delete routes, arbitrary text fields or controlled runner endpoint.
A database-backed shared limit permits at most 200 save admissions per UTC
database day; duplicate saves normally reuse their existing snapshot. Lists show
the latest 20; older snapshots remain addressable by their UUID link.

The saved configuration reproduces catalog/projection/dynamics settings for
`starmap-illustrative-v1`. Educational experiment controls and random-seed reruns
are not notebook state; exports make no claim about controlled research results.

## Launch status

Repository checks and local preview verification do not establish a live launch.
Confirm the deployment URL and a successful durable save/load round trip before
announcing public availability.
