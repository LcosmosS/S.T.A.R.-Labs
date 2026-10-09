# Scientific gate path after recovered-corpus review

**Controlling authority:** `charter/STAR_Research_Charter_v0-2.pdf`. This record separates source provenance, controlled execution and scientific support. Passing an earlier gate never implies a later one.

## Repository gates

| Gate | Required evidence | Current repository state |
|---|---|---|
| G0 — preservation and governance | immutable audit history, quarantine instead of deletion, qualified namespaces, fail-closed validators | Audit/quarantine and review docket merged; the active GitHub ruleset still requires separate administrator attention because repository protections were observed disabled during integration |
| G1 — immutable source identity | publisher/release identity, exact source bytes, SHA-256, schema/row count, license/use terms | `DATA-ARITHMETIC` remains verified; `DATA-MANGA-HI-ALL` is now publisher-byte verified; Pipe3D publisher bytes match local recoveries but are not repository-preserved |
| G2 — prospective protocol | claim/dataset/parameter/null IDs, endpoint, exclusions, seed, alpha and failure rules locked before testing | A01 is preregistered; A03 has a candidate protocol and test-only implementation; astronomical match and leakage protocols remain blocked drafts |
| G3 — canonical lifecycle transition | reviewed registry migration with exact code/config/spec hashes | A01 complete; A03 and astronomical candidates are not transitioned |
| G4 — controlled activation | clean integrated main, pinned inputs, successful preflight, execution eligibility only | PR #64 remains unmerged pending final outside independent review; no support flag may change in activation |
| G5 — result and reproduction | immutable result manifest, negative results retained, independent executor rerun | no new controlled result claimed |
| G6 — astronomical correspondence | spherical geometry, duplicate policy, selection function, matched nulls, uncertainty and out-of-sample test | not established |
| G7 — cross-dataset prediction | independent survey or independently constructed sample and meaningful held-out utility | not established |
| G8 — physical interpretation | empirical correspondence independently established and known constraints satisfied | not open |

The merge order used preservation and design before execution: PRs #69, #70, #63, #62, #65, #66, #68 and #71. PR #64 is intentionally excluded from this merge set because an outside independent review is its final activation gate.

## Verified lineage outcomes

- **H I-MaNGA DR3:** the SDSS DR17 publisher binary at `MANGA_HI/v2_0_1/mangaHIall.fits`, the recovered Dropbox file and the existing Git LFS object are byte-identical: SHA-256 `0f51e1852f7103bd9af9699213a7548a7e6b9969ab1256ec86df04352ddec8f5`, 1,584,000 bytes, 6,632 FITS rows and 34 fields. Canonical provenance advances to `verified`; dataset status stays `planned`, achieved evidence stays `unknown`, and all eligibility flags stay false.
- **MaNGA Pipe3D:** the SDSS DR17 publisher binary, Dropbox recovery and OneDrive recovery are byte-identical: SHA-256 `ac714809044c02dcb2cc8b5007d02981d9316c34dc398a79f4c07bde4d3496fc`, 55,889,280 bytes, 10,220 rows and 536 fields. No repository LFS object is present, and the raw-to-SFR transformation remains unresolved, so the canonical provenance row stays `unknown`.
- **Arithmetic source:** a fresh download of `JohnCremona/ecdata` file `allcurves/allcurves.00000-09999` at commit `25cec5ecfec8b9f016eb1631ac633194c2bed39f` reproduced SHA-256 `259f3846329395b371e8079c77a6f1097adaebc98a054974573e241416efa968`, Git blob `baab5801d7f81e1d5c44f5eb5acf4f1e100bc90b` and 64,687 rows. The existing canonical arithmetic provenance requires no change.

Machine-readable evidence is in `data/provenance/publisher_byte_verification_2026-10-08.json`.

## VizieR frozen-dataset promotion design

The first candidate is corrected August 2019 ALFALFA table `J/ApJ/861/49/table2` with 31,502 rows. Its current templates under `research/acquisition/vizier_alfalfa100/` are non-operational and the sky release manifest admits zero sources.

Promotion requires a separate reviewed version bump that completes every step:

1. Download the complete table from an identified CDS/VizieR mirror as VOTable or FITS with provider row limits disabled. Preserve request bytes/URL, response headers, retrieval time, catalogue DOI, article DOI, corrected-table designation and use terms.
2. Store the untouched response under `data/intake/vizier/alfalfa100/<acquisition-id>/` through real Git LFS. Verify the remote LFS object can be fetched and reproduces its OID/SHA-256 and byte count.
3. Freeze the VizieR ReadMe and field metadata with their hashes. Validate exactly 31,502 source rows, units/UCDs, null markers, coordinate frame/epoch, `AGC` multiplicity and quality-code distributions. Abort on truncation or schema drift.
4. Preserve the raw source unchanged. Produce any normalized `source_id,ra_deg,dec_deg` display table as a distinct derived object with transformation-code hash, environment, source-to-derived row map and derived SHA-256.
5. Lock coordinate role before matching: `RAO/DEO` for nullable optical counterparts or `RAJ2000/DEJ2000` for H I centroids. Freeze spherical geometry, uncertainty model, footprint/selection controls, velocity agreement, multiplicity policy and survey-mask-aware null before inspecting associations.
6. Add versioned dataset/provenance/crosswalk rows and an independent source-review receipt. Only then may `web_tool/content/sky-overlay-releases.v1.json` list the frozen display artifact. Dataset, execution, controlled-support and physical-support eligibility remain false until later gates are passed.

Local Aladin display and a matching hash are inspection aids. They do not establish provenance, association validity, replication or support.
