# STARMAP by S.T.A.R. Labs

A working exploratory prototype: interactive arithmetic projection, searchable
illustrative catalog, RTCH toy dynamics, educational topology/rank diagnostics,
the repository's read-only registry, and a public demo notebook.

## Evidence boundary

The browser catalog contains 12 handwritten illustrative records and 148 seeded
synthetic records. These are not verified LMFDB exports. Synthetic features depend
on rank; omitting rank as a coordinate does not establish independence. Browser
diagnostics are educational, not `EXP-MAP-A01` execution or scientific evidence.

The homepage, projection, registry and research pages now distinguish these
fixtures from the preserved investigator-A primary transaction
`20261016T041335361140Z-e60fd05117fc`, recorded at source revision
[`1b0f2d7853608bfbab79cf2dc04b002f1f193eb2`](https://github.com/LcosmosS/S.T.A.R.-Labs/commit/1b0f2d7853608bfbab79cf2dc04b002f1f193eb2)
and preserved by [PR #104](https://github.com/LcosmosS/S.T.A.R.-Labs/pull/104).
The [pinned primary package](https://github.com/LcosmosS/S.T.A.R.-Labs/tree/f6d8bc8e954d5923ab9fa512ffcc6320d4c4018b/release_packages/EXP-MAP-A01-primary-execution-v0.1)
records **T = -114.40183841751903**, **p = 0.001**, **0/999 exceedances**,
**alpha = 0.01**, and **38,042 analysis rows** from 64,687 source rows.
T is negative mean absolute elevation difference on the fixed k=10 arithmetic
neighbor graph; larger T means greater local rank/elevation coherence.
Exceedances are `T_null >= T_observed`, and the locked correction is
`p = (1 + 0) / (999 + 1) = 0.001`, the smallest attainable p-value for 999
permutations, rather than zero.

The endpoint rejects only `NULL-MAP-001`, the locked arithmetic rank-permutation
null. It neither tests a survey-selection-matched cosmological null nor
distinguishes ACSC from other arithmetic structure. Independent rerun and
replication remain outstanding. The [verification receipt](https://github.com/LcosmosS/S.T.A.R.-Labs/blob/f6d8bc8e954d5923ab9fa512ffcc6320d4c4018b/release_packages/EXP-MAP-A01-primary-execution-v0.1/verification.json)
documents saved-package inspection, not independent replication or physical
ACSC support. Current execution eligibility comes from canonical registry flags;
controlled-support and physical-support eligibility remain false. Older
preregistration/activation package descriptions retain their historical state.

`/registry` is generated from canonical repository files, with their SHA-256 hashes
and the controlled spec's binding checks. It displays declared gates without
editing them or granting execution. Run `npm run registry:sync` after intentional
canonical source changes; `npm run registry:check` rejects a stale snapshot.

The projection, registry and research pages share the same current-status panel;
the homepage reuses its primary-evidence component.
Execution descriptions follow canonical flags; sky candidates are shown as admitted
only when source, coordinate and ordered-ID hashes and coordinate role match the
release manifest. Published M1/A01/A03 packages and their scientific limits are
copied from the root README, which is included in the snapshot SHA-256 inputs.
Updating its publication metadata therefore also requires `npm run registry:sync`.
Canonical dataset provenance includes expandable source, acquisition, transformation,
selection and integrity records, separately from historical LFS classifications.

## Research content and historical SFR addendum

The separate /research catalog is generated from `content/research-content.v1.json` and remains distinct from /registry's controlled evidence records. The 2026-10-08 merge resolution retained PRs #59–#60 as the canonical source and page implementation, while adding explicit finite-positive-bin mathematics and unreplicated SFR report context from PR #61. No eligibility or physics-support flags were promoted. Use `npm run research:check` and review the desktop/mobile browser smoke test.

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

The public app is available at [starmap-star-labs.vercel.app](https://starmap-star-labs.vercel.app/).
Deployed pages are versioned snapshots, not a live GitHub status feed. Inspect
the registry snapshot digest after each deployment to distinguish current source
from old explanatory text. Notebook storage health and durable save/load verification
remain separate from registry freshness and scientific evidence.

## Collaboration and image references (2026-10-18)

Use the [bounded invitation](../release_packages/STAR-collaboration-invitation-v0.1/README.md)
for expertise requests, independent verification and citations. The audited
baseline is main `d69868e3c1d9ae70944deb239369e53a9ecc1e5b`; unmerged PR #107's
A01 viewer is a separate candidate, not a feature promised by this baseline.

The current [README banner](artifacts/imagine_images/starmap.png) and
[social card](public/og.jpg) are generated communication graphics, not app
screenshots, measured coordinates or replication evidence. Their
[provenance and scope](artifacts/exp-map-a01-primary-evidence-images.md) record
respectively SHA-256 `33b7d5361353404ec8606247c964f164efc9d98db9296c0579f1311677389f05`
and `1a737c65a2dae2b027ffa5da101de5b92f3c48e2a0c503311ed719197521322f`.
The social-card path is resolved by `scripts/grok-pwa-shared.mjs` from
`public/og.jpg`; the README banner is not that runtime asset. The October 18
review confirmed these existing bytes and their caveats; no new image or
scientific figure replaces them. Root README image links now resolve within
the checked-out branch instead of forcing branding from mutable main.

A deployed URL or cached social card may refer to an older build. Verify the
served source digest, image bytes and deployment revision separately before
asserting deployment parity; local build success does not establish it.
