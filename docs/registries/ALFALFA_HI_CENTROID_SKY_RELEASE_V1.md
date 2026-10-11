# ALFALFA α.100 — proposed H I-centroid display release v1

**Decision: NOT YET APPROVED FOR WEB ADMISSION.** Governing authority:
[`STAR_Research_Charter_v0-2.pdf`](../../charter/STAR_Research_Charter_v0-2.pdf).
This is a focused, reviewable source-to-coordinate display candidate. A publisher
record, successful byte checks, and green CI **cannot** supply an off-author
scientific/governance review receipt. No A01/A03 execution, crossmatching,
stellar-formation-rate inference, controlled/physical support, or cosmological
correspondence is enabled here.

## Individually auditable byte lineage

| Boundary | Canonical record |
| --- | --- |
| Publisher | [CDS VizieR J/ApJ/861/49/table2](https://vizier.cds.unistra.fr/viz-bin/VizieR-3?-source=J%2FApJ%2F861%2F49%2Ftable2), corrected August 2019; catalogue DOI [10.26093/cds/vizier.18610049](https://doi.org/10.26093/cds/vizier.18610049) |
| Authoritative source | `data/intake/vizier/alfalfa100/2026-10-09-cds-corrected-2019/table2.vot` (10,981,088 actual bytes stored via LFS; the Git pointer itself is not source data) |
| Source SHA-256 | `654217f9b3414856c1a8b09071c81eb834a0b0fbc6ec3aea9777e01fdaea1079` |
| Source observations | 31,502 rows, 25 fields, 0 duplicate AGCs; 344 paired-missing optical counterparts retained |
| Acquisition | [request and response metadata](../../data/intake/vizier/alfalfa100/2026-10-09-cds-corrected-2019/request.json), [source/derived lineage receipt](../../data/provenance/observational_dataset_intake_2026-10-09.json), [registries](../../registry/data_provenance_registry_v0.1.csv) |
| Coordinate role | H I **radio centroids**, VizieR `RAJ2000,DEJ2000`, J2000 equatorial degrees for an ICRS display; **not** nullable optical `RAO,DEO` counterparts |
| Conversion + selection | [Locked display/matching protocol](../../research/acquisition/vizier_alfalfa100/matching_protocol_v1.md): signed sexagesimal-to-degree transform, 2,000 smallest `SHA256("ALFALFA-A100-DISPLAY-v1\\0" + AGC)` ranks, retained in original source order; no scientific-variable selection |
| Original derived candidate | `data/derived/vizier/alfalfa100/2026-10-09-cds-corrected-2019/alfalfa100_hi_centroids_display_2000.csv` |
| Web-asset staging path | `web_tool/public/sky/alfalfa100-hi-centroids-v1.csv` — Git blob identical to original derived candidate, but **removed by production build filter unless admitted** |
| Exact web-coordinate SHA-256 | `ddf040c5954bc9ae2c19415d46071443cd6a3f209069e095fd2b4bbe7b8fadf9` (70,959 bytes, header and 2,000 rows) |
| Ordered ID-chain SHA-256 | `7b5de4187e24df2c0c1936164ecd1ade0ae5c4ee15d2ff64847499fd7e7c6221` (source IDs joined by LF with a final LF) |
| Receipt awaiting independent reviewer | [Pending review record](ALFALFA_HI_CENTROID_SKY_V1_REVIEW_PENDING.json), intentionally has no reviewer identity, reviewed commit, or approval decision |

The checked-in web-asset candidate is byte-for-byte identical at the Git blob
level to the previously frozen 2,000-row derivative. This is **not** a claim
that an independent reviewer has approved its astrometry, licensing, selection,
or publication. The 31,502-row source is preserved outside `web_tool/public`.

## Human authorization and release procedure

1. An off-author, accountable reviewer must independently hydrate and hash
   the corrected CDS/VizieR LFS source, inspect its 25-field schema, role of
   `RAJ2000/DEJ2000`, absence of optical coordinate substitution, exact
   conversion/selection algorithm, derived 2,000 rows, source-ID hash and
   publication/license obligations.
2. Record the reviewer identity, exact reviewed commit, review URL/signature,
   and affirmative **display-only** decision in a new immutable receipt. Pin
   its SHA-256 in the single release entry, and move that entry from
   `reviewCandidates` into `sources` in the same PR. The review must
   independently bind that **final byte lineage**, not just an earlier
   publisher-source provenance approval.
3. Run the source-hydrated `npm run sky:check`, ensure it reports
   `count: 1` with exactly `DATA-VIZIER-ALFALFA100`, rerun positive and
   negative release/runtime tests, verify the deployment filter emits only
   the approved static CSV, and record successful exact-head CI.
4. Obtain the required accountable PR approval and review of the exact final
   manifest and receipt before merging. The release may then be selected
   by ALADIN Lite, where the browser hashes the fetched same-origin file
   and all 2,000 source IDs before rendering any marker.

**Current effect:** `sources: []` remains fail-closed. The manifest contains
exactly one **review candidate**, which is not an admitted release. Production
builds filter unadmitted files. The requested final one-admitted-catalogue
acceptance test cannot honestly pass before step 2.
