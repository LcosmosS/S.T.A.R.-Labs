# ALFALFA α.100 — reviewed H I-centroid display-only release v1

**Governance state (2026-10-11):** The exact H I-centroid source/derivative
byte lineage has an identifiable, recorded **display-only** review receipt
from LibertySquared. The single release is included in the PR #95 admission
manifest as `sources[0]`. This is an **unmerged proposal**, not evidence that
the production deployment is approved or that exact-final-head CI/repository
branch review is complete. The GitHub PR remains in draft/review hold until
both requirements are met.

Governing authority:
[`charter/STAR_Research_Charter_v0-2.pdf`](../../charter/STAR_Research_Charter_v0-2.pdf).
This display-only review does **not** authorize A01/A03 execution,
crossmatching, stellar-formation-rate inference, controlled support, physical
support or cosmological correspondence.

## Auditable byte lineage

| Boundary | Canonical record |
| --- | --- |
| Publisher | [CDS VizieR J/ApJ/861/49/table2](https://vizier.cds.unistra.fr/viz-bin/VizieR-3?-source=J%2FApJ%2F861%2F49%2Ftable2), corrected August 2019; catalogue DOI [10.26093/cds/vizier.18610049](https://doi.org/10.26093/cds/vizier.18610049) |
| Authoritative source | `data/intake/vizier/alfalfa100/2026-10-09-cds-corrected-2019/table2.vot` — 10,981,088 hydrated bytes via Git LFS; the Git pointer itself is not source data |
| Publisher SHA-256 | `654217f9b3414856c1a8b09071c81eb834a0b0fbc6ec3aea9777e01fdaea1079` |
| Source observations | 31,502 rows, 25 fields, no duplicate AGCs; 344 paired-missing optical counterparts retained |
| Acquisition + provenance | [Publisher request metadata](../../data/intake/vizier/alfalfa100/2026-10-09-cds-corrected-2019/request.json), [source lineage receipt](../../data/provenance/observational_dataset_intake_2026-10-09.json), [canonical provenance registry](../../registry/data_provenance_registry_v0.1.csv) |
| Coordinate role | J2000 `RAJ2000,DEJ2000` **H I radio centroids**, not nullable optical `RAO,DEO` counterparts |
| Selection + conversion | [Matching/display protocol](../../research/acquisition/vizier_alfalfa100/matching_protocol_v1.md): deterministic sexagesimal-to-degree conversion; 2,000 smallest SHA-256 ranks of `ALFALFA-A100-DISPLAY-v1\\0` + AGC, retained in original source order; no outcome-dependent selection |
| Derived display CSV | `data/derived/vizier/alfalfa100/2026-10-09-cds-corrected-2019/alfalfa100_hi_centroids_display_2000.csv` |
| Tracked same-origin web file | `web_tool/public/sky/alfalfa100-hi-centroids-v1.csv` — byte-identical 70,959-byte copy with header + 2,000 rows |
| Coordinate SHA-256 | `ddf040c5954bc9ae2c19415d46071443cd6a3f209069e095fd2b4bbe7b8fadf9` |
| Ordered ID-chain SHA-256 | `7b5de4187e24df2c0c1936164ecd1ade0ae5c4ee15d2ff64847499fd7e7c6221` (one `source_id` per LF line and final LF) |
| Review receipt | [ALFALFA_HI_CENTROID_SKY_V1_REVIEW_RECEIPT.json](ALFALFA_HI_CENTROID_SKY_V1_REVIEW_RECEIPT.json); `decision=approved_for_display_only` |
| Exact corrected receipt SHA-256 | `b9a4328f4d5dcf1b3d0680218977ca2a99165988ed6d010b46260d7b972c2b68`, bound in [one-source release manifest](../../web_tool/content/sky-overlay-releases.v1.json) |
| Accountable review evidence | Receipt names LibertySquared (Shaughn McNamara), time and reviewed commit `a2644f22ff89c7ab866fb13a737dec361d472a3a`; see [PR #95 review](https://github.com/LcosmosS/S.T.A.R.-Labs/pull/95). The review receipt is a scoped source/coordinate assessment **not a human APPROVED review of the final repair head** |

## Admission and build contract

1. **One scoped source, no scientific escalation.** Release schema
   `star-sky-overlay-releases-v1` contains exactly one record under
   `sources` for `DATA-VIZIER-ALFALFA100`, with coordinate role
   `hi_centroid`, review status `approved_display_only`, and both
   scientific/physical support flags false. `reviewCandidates` is empty;
   synthetic pending-review fixtures still must remain rejected.
2. **Exact source-hydrated CI.** STARMAP hydrates the pinned publisher VOTable,
   then `npm test`, `npm run sky:check`, `npm run build`, and browser marker
   smoke must pass on the **same final PR head**. Integrity checks include raw
   SHA, derivative file SHA, selected-ID chain, review receipt SHA and
   deliberate source/receipt/coordinate tampering failures.
3. **Nondestructive deployment.** `web_tool/public/sky` remains checked-in and
   unchanged by building. `filter-deployed-sky-assets.mjs` stages a separate
   `web_tool/.sky-public-build` directory containing **only admitted sky
   files** plus other static assets. Vite uses that generated directory for
   production builds. The generated directory is ignored by Git and Vercel
   source upload; no tracked files are deleted by `npm run build`.
4. **Browser checks before visualization.** The browser requests only its
   same-origin admitted CSV with redirects denied, recomputes both SHA-256
   chains and parses 2,000 distinct in-range centroids before passing markers
   to the pinned Aladin Lite API. CI's stubbed Aladin browser test asserts all
   2,000 API inputs; it does not independently validate external CDS imagery.
   Modified bytes must yield zero marker inputs.
5. **Final GitHub authorization pending.** Exact-final-head Actions success
   and a reviewer with write access submitting `APPROVED` on the final
   manifest, amended receipt and deployment/CI changes are required. An
   earlier source-review receipt alone cannot merge this PR or guarantee a
   deployed page. The repository author must not self-approve.

**Scientific scope:** A verifiable visual overlay of published ALFALFA H I
centroids. Neither the 2,000-row preview nor any LFS/coordinate/receipt
checksum validates an optical association, derived galaxy property, rank
prediction, or physical correspondence.

