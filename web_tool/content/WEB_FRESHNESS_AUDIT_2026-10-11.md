# STARMAP repository freshness audit — 2026-10-11

Authority: `charter/STAR_Research_Charter_v0-2.pdf`.
Inspected repository main: `d864dcd3084ef4ae6c265ed4b6efd924b837a89b`.

## Production verification

The public `https://starmap-star-labs.vercel.app` alias was READY on production
deployment `dpl_GhfrpJe6tTvF48ct6xqu4NWnqvDV`, project
`prj_vQnwM1giU4MBEpzqbUI9K3CUN5Gf`, scope `lcosmoss`. Read-only Vercel
deployment metadata confirmed Git branch `main` and the inspected commit above.
The connector rejected project-scope reads with HTTP 403; the skill's CLI
fallback succeeded. No deployment or database configuration was changed.
Public `/api/health` reported `status: ok`, `storage: neon`, `durable: true`,
`demoVersion: starmap-illustrative-v1`. This is a storage-readiness check,
not a new save/load round trip or a scientific verification.

The stale content was present in current main itself, rather than an older
production revision. The original registry source digest was
`fa9d99dfd9575ed1428fdad052c60c556a85d407ff0420c5e2ea193dccb3d56b`.

## Findings and response

| Surface | Stale or missing presentation | Response |
| --- | --- | --- |
| Projection | PR #64-era warning and assertion that no sky release was admitted | Shared panel reads current A01 flags, A03 registry state and admitted sky manifest |
| Registry / A01 | Bound historical assessment says execution is disabled while flags are true | Current narrative derives from both eligibility flags; original canonical row remains in downloadable snapshot |
| Registry / ALFALFA | Historical candidate says pending review beside an admitted identical release | Show admitted status only for exact source, coordinate, ordered-ID digests and coordinate role; preserve candidate history |
| Registry / recovered sources | Blanket upstream-unverified narrative no longer describes all source bytes | Distinguish original recovery classification from current canonical dataset provenance |
| Research / release discovery | M1/A01/A03 archives and their limits absent | Shared panel copies current README DOI, release links, review references and scientific-status text |
| Numerical protocols | A01/A03 cards lack bound protocol links | Link only protocol paths present in hashed snapshot inputs |
| Generated route tree | Committed tree omits existing research route | Regenerate with normal build; clean-checkout typechecking recognizes `/research` |

## Boundaries and freshness controls

No canonical registry, controlled specification, experiment protocol, frozen
release package, scientific payload, LFS object or support flag is changed.
A01's reviewed activation (PR #78; package PR #94 and citation PR #96) is
execution-only. A03 remains execution-ineligible. M1's candidate theorem archive
does not change its planned registry stages. ALFALFA PR #95 admits 2,000 H I
centroids from 31,502 source rows for display only. The three reserved placeholder
IDs remain explicitly unresolved while their records remain planned/unknown.

The generated snapshot now includes dataset rows, README publication metadata,
A03 protocol and both sky manifests in its source-hash inputs. The Vercel upload
filter retains the exact new inputs; an isolated filtered-tree test checks this.
`registry:check` rejects source drift. Published-page descriptions are snapshots,
not live GitHub queries, and DOI links alone do not verify deposited bytes.

Verification covers web unit tests, production build, typechecking, registry and
research freshness gates, hydrated sky source/receipt validation, desktop/mobile
rendering, research filters, shared-status consistency across all three pages,
and sky marker byte checks/tamper rejection. The sky test uses a deterministic
Aladin API spy and does not claim to test third-party sky imagery availability.

This refresh is a review-branch change. Production remains at the inspected main
until the update is merged and its Git deployment is verified.
