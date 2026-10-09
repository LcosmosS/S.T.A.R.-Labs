# Scientific gate path after recovered-corpus review

**Controlling authority:** `charter/STAR_Research_Charter_v0-2.pdf`. This record separates source provenance, controlled execution and scientific support. Passing an earlier gate never implies a later one.

## Repository gates

| Gate | Required evidence | Current repository state |
|---|---|---|
| G0 — preservation and governance | immutable audit history, quarantine instead of deletion, qualified namespaces, fail-closed validators | Audit/quarantine and review docket merged. GitHub ruleset `Non-negotiable` (ID `15259335`) was active when rechecked after integration, but it does not require a pull request, independent approval or named status checks and permits always-on administrator/integration bypass; final independent review therefore remains a Charter gate outside current GitHub enforcement |
| G1 — immutable source identity | publisher/release identity, exact source bytes, SHA-256, schema/row count, license/use terms | `DATA-ARITHMETIC`, `DATA-MANGA-HI-ALL`, Pipe3D, GEMA 2.0.2 and corrected ALFALFA table2 are publisher-byte verified. The three new source objects are repository-preserved through Git LFS; evidence and execution flags remain unchanged |
| G2 — prospective protocol | claim/dataset/parameter/null IDs, endpoint, exclusions, seed, alpha and failure rules locked before testing | A01 and A03 are preregistered at their stated scopes. ALFALFA display selection and matching boundaries are locked, but inferential matching remains blocked until a source-level positional-error model is frozen; SFR leakage and other astronomical experiment protocols remain incomplete |
| G3 — canonical lifecycle transition | reviewed registry migration with exact code/config/spec hashes | A01 complete; A03 and astronomical candidates are not transitioned |
| G4 — controlled activation | clean integrated main, pinned inputs, successful preflight, execution eligibility only | PR #64 was merged and then reverted by PR #77 after its independent-approval gap was recognized. Replacement PR #78 remains open and unapproved; no support flag may change in activation |
| G5 — result and reproduction | immutable result manifest, negative results retained, independent executor rerun | no new controlled result claimed |
| G6 — astronomical correspondence | spherical geometry, duplicate policy, selection function, matched nulls, uncertainty and out-of-sample test | not established |
| G7 — cross-dataset prediction | independent survey or independently constructed sample and meaningful held-out utility | not established |
| G8 — physical interpretation | empirical correspondence independently established and known constraints satisfied | not open |

The preservation/design sequence on main includes PRs #69, #70, #63, #62, #65, #66, #68, #71, provenance-only PR #74, gate clarification PR #75, Aladin admission controls PR #76, corrective revert PR #77, claim/audit corrections PR #79 and protocol-only A03 PR #83. PR #78 is the open replacement A01 activation proposal. PRs #80 and #81 are also open review records; none of #78, #80 or #81 authorizes this dataset intake or Aladin admission.

## Verified lineage outcomes

- **H I-MaNGA DR3:** the SDSS DR17 publisher binary at `MANGA_HI/v2_0_1/mangaHIall.fits`, the recovered Dropbox file and the existing Git LFS object are byte-identical: SHA-256 `0f51e1852f7103bd9af9699213a7548a7e6b9969ab1256ec86df04352ddec8f5`, 1,584,000 bytes, 6,632 FITS rows and 34 fields. Canonical provenance advances to `verified`; dataset status stays `planned`, achieved evidence stays `unknown`, and all eligibility flags stay false.
- **SDSS DR18 200k historical CasJobs sample:** the existing remote-verified LFS object has SHA-256 `9dca2008683fde4b0f7a90af5de85ee846a30a47f6f6fae3968c83dea06fa5d2`, 33,007,497 bytes, 200,000 rows and the 18 columns in the recovered `TOP 200000` SQL. The archived/Dropbox `Zone.Identifier` binds renamed `SDSSDR18_200000.csv` to original `MyTable_pmqr771_0.csv`. This validates a historical source-binding candidate, not canonical upstream identity: the job ID/time/database snapshot/output checksum are missing and no `ORDER BY` fixes exact rerun membership. Canonical provenance/evidence stay `unknown`; all eligibility remains false.
- **MaNGA Pipe3D:** the SDSS DR17 publisher binary, Dropbox recovery, OneDrive recovery and new repository Git LFS object are byte-identical: SHA-256 `ac714809044c02dcb2cc8b5007d02981d9316c34dc398a79f4c07bde4d3496fc`, 55,889,280 bytes, 10,220 rows and 536 fields. Canonical provenance advances to `verified`; the raw-to-SFR transformation remains unresolved, dataset status stays `planned`, evidence stays `unknown`, and all eligibility flags stay false.
- **MaNGA GEMA 2.0.2:** the SDSS DR17 publisher binary, recovered Dropbox file and repository Git LFS object are byte-identical: SHA-256 `244e9286f225b9e1dbef73bb93e1101d840a2a62ec5dabf3aa16ec88cfef1597`, 7,223,040 bytes and 15 FITS binary-table extensions. Canonical provenance advances to `verified`; analysis-table selection and downstream joins remain unresolved, and all eligibility flags stay false.
- **Corrected ALFALFA alpha.100:** the untouched 31,502-row VizieR VOTable has SHA-256 `654217f9b3414856c1a8b09071c81eb834a0b0fbc6ec3aea9777e01fdaea1079`; the frozen ReadMe has SHA-256 `6aa40d3e1552c104e5197a330bb30f440f87206d4763a52322a6c02afd43b9d4`. Schema and coordinate semantics validate with zero duplicate AGC IDs, 344 paired-missing optical coordinate rows and H I quality counts 25,434/6,068. Provenance is `verified`; the Aladin candidate is pending independent review and every execution/support flag remains false.
- **Arithmetic source:** a fresh download of `JohnCremona/ecdata` file `allcurves/allcurves.00000-09999` at commit `25cec5ecfec8b9f016eb1631ac633194c2bed39f` reproduced SHA-256 `259f3846329395b371e8079c77a6f1097adaebc98a054974573e241416efa968`, Git blob `baab5801d7f81e1d5c44f5eb5acf4f1e100bc90b` and 64,687 rows. The existing canonical arithmetic provenance requires no change.

Machine-readable evidence is in `data/provenance/publisher_byte_verification_2026-10-08.json`.

## VizieR frozen-dataset promotion record

The first candidate is corrected August 2019 ALFALFA table `J/ApJ/861/49/table2` with 31,502 rows. The raw source and ReadMe are now frozen, validated and registered. The sky release manifest still admits zero sources; `web_tool/content/sky-overlay-candidates.v1.json` records a hash-bound candidate awaiting off-author review.

Completed source-promotion steps and the remaining display gate are:

1. **Complete:** VizieR request uses `-out.max=unlimited` and `-out.all=1`; exact URL, response headers, retrieval time, catalogue/article DOIs, correction designation and usage/citation terms are frozen.
2. **Repository-preserved:** untouched VOTable is a real Git LFS object. Remote fetch plus SHA-256/size verification is required before publication is reported complete.
3. **Complete:** VizieR ReadMe and field metadata are frozen. CI validates 31,502 rows, 25 fields, UCD-based J2000 coordinate roles, paired optical missingness, AGC uniqueness and H I quality distribution.
4. **Complete:** raw bytes remain unchanged. The full H I-centroid derivative and deterministic 2,000-row display candidate have separate hashes and selected-ID binding.
5. **Preregistered with a hard block:** great-circle geometry, multiplicity, selection and survey-mask-aware null boundaries are fixed in `matching_protocol_v1.md`. Table2 supplies no per-row astrometric error, so inferential cross-matching remains forbidden until a later protocol freezes a cited uncertainty model.
6. **Pending:** an off-author source/display review receipt bound to the exact commit and hashes. Only that later reviewed transition may add the candidate to `web_tool/content/sky-overlay-releases.v1.json`. Dataset, execution, controlled-support and physical-support eligibility remain false.

Local Aladin display and a matching hash are inspection aids. They do not establish provenance, association validity, replication or support.
