# Observational dataset lineage and Aladin review gate

**Authority:** `charter/STAR_Research_Charter_v0-2.pdf`. This record advances source provenance only. It does not report a match result, scientific support, or physical interpretation.

| Dataset | Frozen source | Validation | Canonical status |
|---|---|---|---|
| `DATA-SDSS18-200K` | recovered CasJobs CSV; SHA-256 `9dca2008683fde4b0f7a90af5de85ee846a30a47f6f6fae3968c83dea06fa5d2`; 33,007,497 bytes | 200,000 rows and 18 query-matched columns; `Zone.Identifier` binds renamed file to `MyTable_pmqr771_0.csv`; remote LFS proof already exists | historical source-binding candidate; canonical provenance/evidence `unknown`; all eligibility false |
| `DATA-SFR-MANGA-PIP3D` | SDSS DR17 `SDSS17Pipe3D_v3_1_1.fits`; SHA-256 `ac714809044c02dcb2cc8b5007d02981d9316c34dc398a79f4c07bde4d3496fc`; 55,889,280 bytes | Publisher, Dropbox and OneDrive bytes match; 10,220 FITS rows and 536 fields | provenance `verified`; dataset `planned`; evidence `unknown`; all eligibility false |
| `DATA-COSMIC-ENV` | SDSS DR17 GEMA 2.0.2 `GEMA_2.0.2.fits`; SHA-256 `244e9286f225b9e1dbef73bb93e1101d840a2a62ec5dabf3aa16ec88cfef1597`; 7,223,040 bytes | Publisher and Dropbox bytes match; 15 FITS binary-table extensions | provenance `verified`; dataset `planned`; evidence `unknown`; all eligibility false |
| `DATA-VIZIER-ALFALFA100` | corrected August 2019 VizieR `J/ApJ/861/49/table2`; SHA-256 `654217f9b3414856c1a8b09071c81eb834a0b0fbc6ec3aea9777e01fdaea1079`; 10,981,088 bytes | 31,502 rows, 25 fields, zero duplicate AGC IDs, 344 paired-missing optical coordinates, quality codes 1: 25,434 and 2: 6,068 | provenance `verified`; dataset `planned`; evidence `unknown`; web admission pending; all eligibility false |

The frozen VizieR ReadMe has SHA-256 `6aa40d3e1552c104e5197a330bb30f440f87206d4763a52322a6c02afd43b9d4`. The full H I-centroid derivative has SHA-256 `ae65f7e0ffd4f90219f91aaa0d29f6cad6930696f6a181ba37740e4758206ba2` over all 31,502 rows. The bounded 2,000-row display candidate has SHA-256 `ddf040c5954bc9ae2c19415d46071443cd6a3f209069e095fd2b4bbe7b8fadf9`; its selected-ID chain is `7b5de4187e24df2c0c1936164ecd1ade0ae5c4ee15d2ff64847499fd7e7c6221`.

The [matching/display protocol](../../research/acquisition/vizier_alfalfa100/matching_protocol_v1.md) fixes coordinate role, spherical geometry, multiplicity, missingness, deterministic selection and the null-policy boundary. It blocks inferential matching because table2 has no per-row astrometric uncertainty column. The source may be inspected in Aladin only after an off-author receipt approves these exact source and display hashes.

## Independent review references

- [PR #78](https://github.com/LcosmosS/S.T.A.R.-Labs/pull/78) is the separate A01 activation review and is not dataset approval.
- [PR #80](https://github.com/LcosmosS/S.T.A.R.-Labs/pull/80) is a read-only independent gate-readiness package and is not dataset approval.
- [PR #81](https://github.com/LcosmosS/S.T.A.R.-Labs/pull/81) is an M1 theorem pre-review bundle and is not dataset approval.

These links give reviewers the surrounding gate record. An APPROVED review on another scope cannot be reused. `web_tool/content/sky-overlay-candidates.v1.json` stays `pending_independent_review`, and `sky-overlay-releases.v1.json` remains empty.

## Historical candidate and registry placeholders

`DATA-SDSS18-200K` is already preserved through real Git LFS. The 33,007,497-byte object has SHA-256 `9dca2008683fde4b0f7a90af5de85ee846a30a47f6f6fae3968c83dea06fa5d2`, 200,000 data rows and the 18 columns selected by the recovered CasJobs SQL. The archived/Dropbox `Zone.Identifier` binds the renamed `SDSSDR18_200000.csv` to `MyTable_pmqr771_0.csv`. CI now verifies that historical source binding. Canonical provenance remains `unknown`: the CasJobs job ID, execution time, database snapshot and job-output checksum are not bound to the bytes, and `TOP 200000` without `ORDER BY` cannot reproduce exact membership.

`DATA-PROVENANCE-ALL`, `DATA-PHYS-CONSTRAINTS`, and `DATA-ECC-THEORY` are reserved registry placeholders, not missing files. None currently has a concrete schema or mathematical input definition, frozen source/construction procedure, or byte-level integrity object. Their provenance remains `unknown`, and no experiment may treat those IDs as executable datasets. The machine-readable dispositions are in `data/provenance/dataset_resolution_attempts_2026-10-09.json`.
