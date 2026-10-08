# Independent PR review, scientific gates and CI-frozen observational sky
**Review docket date:** 2026-10-08. **Governing authority:** charter/STAR_Research_Charter_v0-2.pdf (Research Charter v0.2).
**Scope:** review and prospective integration specification only. No data acquisition, experiment execution, controlled-support adjudication, or merge authorization.

## 1. Evidence semantics: mandatory separation
The Charter's arithmetic -> geometry -> topology -> observation -> dynamics -> physics progression is mandatory. Its D/E/M/P/H/C/T/S epistemic classes must not be conflated. A working visualization or CI success is not empirical support for arithmetic-cosmic correspondence. Canonical support requires preregistered hypothesis-specific evidence, appropriate nulls, independent data, replication and an explicit approved claim/evidence decision.

Separate four machine-readable states: (1) raw byte identity verified, (2) upstream astronomical provenance independently verified, (3) observational display acceptance for a frozen derived coordinate table, (4) **claim-specific** controlled support, independently adjudicated. State (4) cannot be inferred from (1)-(3) and no dataset-wide bool authorizes all claims. A fifth, physical-support state requires a separate, stronger theory/observation review. Do not silently convert one state into another.

### Snapshot of open PRs (heads checked 2026-10-08 UTC)
All remain DRAFT, GitHub mergeable and have no submitted reviewer approvals; all head-specific workflow sets PASS at the time of this audit. Recheck the **exact SHA after any new commit or another PR merge**, including cross-branch protected validators. No independent theorem or observational result follows from CI.

| PR | Exact reviewed head | Reported CI | Independent review / disposition |
| --- | --- | --- | --- |
| [#62](https://github.com/LcosmosS/S.T.A.R.-Labs/pull/62) prospective MCJ and observational-control designs | 396f62b816abc134d343820cefa757b15940f3fd | 6/6 passing | Review protocol choices and frozen A01 lifecycle compatibility; design document only; must not silently activate A03, DATA-A01 or CTRL-A02 |
| [#63](https://github.com/LcosmosS/S.T.A.R.-Labs/pull/63) P0/M1, topology, ECC/RTCH gates | f2130bcbcd18a32a4f6c94118cde56fe4f44d148 | 4/4 passing | Independent proof/counterexample and physical action derivations pending; candidate protocols, not theorem acceptance |
| [#64](https://github.com/LcosmosS/S.T.A.R.-Labs/pull/64) A01 execution-only activation | 119d74ec7bde40b5d4f3ea25a2e821f74c3aeac8 | 7/7 passing, including real source-locked preflight | Independently compare exact two flags and source/code/spec/registry hashes; formal authorization and merge before any original controlled run |
| [#65](https://github.com/LcosmosS/S.T.A.R.-Labs/pull/65) MCJ arithmetic fixture implementation | 0994bbda0b9867552b0d3f00d351d93a93e1fa34 | 3/3 passing | Verify j sign, exact arithmetic, j=0 exclusion, duplicate-coordinate/tie behavior, SplitMix64 fixtures; stacked on #62; no controlled full-cohort execution |
| [#66](https://github.com/LcosmosS/S.T.A.R.-Labs/pull/66) astronomy lineage and SFR leakage fixtures | c629eac425aca740f8fe7f1b1e89e7ee30711f58 | 5/5 passing | Dropbox extraction is not a raw-file digest. Resolve SDSS release/SQL, MaNGA HI duplicate IDs, missing Pipe3D group keys, null and negative 1,495-row artifact before any observational claim |
| [#68](https://github.com/LcosmosS/S.T.A.R.-Labs/pull/68) Aladin Lite local SHA overlay and ALFALFA template | d51ecd27e0d5560568347732d0495dbedea53fd0 | 5/5 passing including mocked Chromium tests | Independent review of live CDS, HiPS URL/permissions, third-party coordinate disclosure, display versus provenance/support wording, immutable CI manifest migration |

## 2. Specific independent review sign-offs
These are obligations, **not** checkmarks. Reviewer names, timestamps, source commit, independent host, actual outputs and dissent/negative findings must be recorded in signed review decisions attached to the relevant PR, not backfilled here.

- [ ] **Mathematical reviewer (P0/M1):** independently rederive the Szekeres–Szafron Einstein–dust pair's exact common elliptic record, regularity, density positivity, shear/eigenprojector invariant, full Einstein tensor and non-isometry on an open set. Check coordinate/diffeomorphism loopholes and convention signs. Audit each of five P0 representative models separately; a class-relative obstruction is never universal impossibility.
- [ ] **Topology reviewer:** inspect EXP-TOPO-A01's pre-outcome sample hash/rule, dimension-0 Vietoris–Rips convention and MST equivalence, zero-length bars, rank permutations, filtration and null calibration, numerical agreement with an independent PH library. No historical Wasserstein threshold substitution; still a candidate, not canonical preregistration.
- [ ] **ECC/RTCH theory reviewer:** ECC d²M=0 and distinction between closed/exact/nonexact classes; choose a new version if local potentials/cocycles or higher-degree curvature are proposed. For RTCH derive conventional Einstein/matter/first-law limits from the **same** action, coefficients, units, boundary conditions and stress tensor; reconcile signed Lambda/Riemann conventions and verify a regular decoupling limit before fits.
**Concrete code-level finding in #65:** src/experiments/exp_map_a03.py:project_arithmetic computes Delta, then returns None immediately when c4=0 **before rejecting Delta=0**. On singular a-invariants (0,0,0,0,0), Delta=0 and c4=0, so the function silently classifies a singular curve as a j=0 exclusion instead of aborting, contrary to the A03 protocol's zero-discriminant fail-closed rule. If c4 is nonzero and Delta=0, the logarithm raises an uncontrolled math-domain error rather than the declared MCJProtocolError. Reviewer must require an explicit Delta==0 guard **before** the c4==0 branch and regression tests for both singular cases. The SHA-pinned ecdata cohort is expected nonsingular; this is a robustness/protocol-integrity defect, not evidence that any controlled result is wrong (no controlled A03 run exists). Treat #65 as **review blocker until fixed and rechecked** even though present CI is green.

**Specific #68 authority boundary:** its allowlist contains two previously registered ID strings, but does not resolve their provenance and achieved-evidence records. User-entered expected SHA is only user-controlled agreement. Neither condition is authority to label a source publisher-verified. Reviewer must require a CI-bound manifest cross-check and no support promotion in UI or registries. Current mock-browser success certifies only local verification flow.

- [ ] **Arithmetic and statistics reviewer (#62/#65):** fixed ecdata source, 38,042 representatives, rank-blind j mapping and j=0 exclusion, principal complex log branch, exact c4³/Delta, binary64 distance tie sorting, 10-NN graph and conductor-decile conditional null, 999 SplitMix64 permutations with independent seed 4103, p=(1+tail)/1000 and declared family multiplicity. Independently implement edge and RNG vectors. No output-informed choices.
- [ ] **Controlled-runner reviewer (#64):** compare activation PR to locked A01 preregistration on the parent commit, verify ONLY EXP-MAP-A01 and DATA-ARITHMETIC execution booleans are true; SHA-256 for ecdata allcurves=259f3846329395b371e8079c77a6f1097adaebc98a054974573e241416efa968, gitlink 25cec5ecfec8b9f016eb1631ac633194c2bed39f, source rows=64,687 and number-one representatives=38,042; confirm exact SHA-bound config, parameters/null/seed 1729, graph and primary statistic unchanged. No support flags. The 999-permutation original run and independent rerun are **not done**; track [Issue #67](https://github.com/LcosmosS/S.T.A.R.-Labs/issues/67).
- [ ] **Astronomy reviewer (#66):** independently identify SDSS DR18 extraction job, release/selection/complete 18-column CSV and byte SHA. TOP 200000 with no ORDER BY cannot imply a representative/stable galaxy sample; observed class=STAR and negative redshift prohibit calling raw rows galaxy-only. Reconcile MaNGA HI multi-observation MANGAID/PLATEIFU counts, HI/optical coordinate roles, units, epochs, footprint, uncertainties and chance associations. Preserve 1,495-row legacy failures. Do NOT deduplicate in place.
- [ ] **SFR methods reviewer (#66/#62):** recover raw Pipe3D group IDs/source and H-alpha target lineage, forbid target-derived features such as log_SFR_Ha_raw, group/sky holdout, fit preprocessing within folds, independent astrophysical baseline, valid astronomy-to-arithmetic association and conditioned null. Old R² scores remain exploratory/unreplicated.
- [ ] **Web/privacy reviewer (#68):** verify actual Aladin version 3.8.1, CDN integrity and fallback, real CDS/HiPS use at desktop/mobile sizes, cross-origin requests, sky-coordinate disclosure, explicit provider credits/licenses, accessible error/failure states, no stale catalog layers when switching datasets, and that arithmetic fixtures never masquerade as celestial positions. Current browser test mocks CDS and is not a live integration certificate.
- [ ] **Registry/governance reviewer:** inspect line-by-line diff and post-merge combined state, required CI checks, status transitions and snapshots; reject any accidental activation/support promotion or changing historical evidence labels. Confirm #65 remains stacked on #62 and merge #62 before #65. Do not treat absence of GitHub review threads as an independent approval.

## 3. Remaining scientific and engineering gates, in order
**G0 (administrative):** independent signed reviews + exact-head CI on merge candidates, branch-protection integration and governance decision. No PR currently has review approval.
**G1 (A01):** #64 approved/merged only after G0; from merged clean checkout execute full source-locked original A01 and independent rerun with both signed manifests and exact output comparisons. A successful preflight is not a permutation-test result. Preserve null/rejection outcomes, and perform separate support review.
**G2 (A03):** #62 protocol and #65 fixture independent audit, separate canonical PAR-MAP-003/NULL-MAP-003/EXP-MAP-A03 transition, code/spec/source hashes, preflight, then another separate eligibility PR. Full B=999 is prohibited before those steps.
**G3 (DATA-A01):** independent raw SDSS/HI release identity, row-level raw digest, multi-observation policy, survey-aware null, fixed tolerances, reproduction and negative-quarantine audit. Do not claim an ordinary 2-arcsec match is valid for broad HI centroid positional uncertainty.
**G4 (CTRL-A02 then SFR-A01):** original MaNGA/Pipe3D target lineage and IDs; leakage-free folds/baselines/null with independent audit; prospective separate SFR study.
**G5 (TOPO, ECC, RTCH and five P0 cases):** independently validated mathematical constructions/physical recoveries and explicit experimental lifecycle; no speculative physical support.
**G6 (web release):** acceptance of an observational image/point overlay is separate from provenance, preregistration, controlled scientific support and physical support.

## 4. Upgrade STARMAP from user-declared hash to CI-pinned, registry-gated sky data
**Present code in PR #68:** client chooses a planned dataset ID and local CSV, then enters an expected SHA. WebCrypto proves only equality between those two user-controlled inputs. Main registry says DATA-SDSS18-200K and DATA-MANGA-HI-ALL have unknown provenance, execution=false, controlled_support=false, physical_support=false. The verified DATA-ARITHMETIC is NOT an observational sky catalogue. Never show a VERIFIED UPSTREAM or SUPPORTED badge from current PR #68 behavior.

### Versioned source-to-overlay manifest proposal (v1)
Do NOT insert placeholders into an operational snapshot. Initially commit an empty, blocked accepted-sources index until one source passes independent upstream review. A prospective record for a future approved source should contain:

~~~json
{
  "schemaVersion": "star-sky-release-v1",
  "datasetId": "DATA-EXAMPLE-ACCEPTED-ONLY-AFTER-REVIEW",
  "qualifiedDatasetId": "REPO-CSV-v0.2:DATA-EXAMPLE-ACCEPTED-ONLY-AFTER-REVIEW",
  "source": {
    "provider": "publisher",
    "catalogueId": "pinned release/table",
    "acquisitionReceipt": "immutable source receipt path",
    "rawPath": "exact source path (LFS object or immutable object store)",
    "rawSha256": "64 hex after independently verified acquisition",
    "sourceRows": 0,
    "sourceUnitsFrameEpoch": "explicit documented values"
  },
  "transform": {
    "codeCommit": "full Git SHA",
    "configSha256": "64 hex",
    "coordinateRole": "hi_centroid OR optical_counterpart OR sdss_position",
    "frame": "ICRS",
    "equatorialEpoch": "J2000/explicit source epoch",
    "selectionId": "predeclared frozen subset rule",
    "selectedIdsSha256": "64 hex"
  },
  "overlay": {
    "path": "/data/sky/v1/<dataset-and-content-hash>.csv",
    "sha256": "64 hex of exact derived bytes",
    "schema": ["source_id", "ra_deg", "dec_deg"],
    "rows": 0,
    "maxDisplayed": 2000
  },
  "acceptance": {
    "rawBytesVerified": false,
    "upstreamProvenanceReviewed": false,
    "coordinateTransformReviewed": false,
    "displayAccepted": false,
    "independentReviewRecord": null
  },
  "science": {
    "controlledSupportEligible": false,
    "physicalSupportEligible": false,
    "supportedClaimIds": [],
    "evidenceManifests": []
  }
}
~~~

This sample is an **invalid candidate template**, not a real manifest; zero source rows / false flags mean it must be rejected by production build. Implement versioned schemas, immutability and distinct source/derived identifiers; do not trust an unreviewed self-declaration of acceptance booleans.

### Proposed CI release transaction (new software, NOT yet implemented)
1. Explicit, approved dataset-registry/provenance transition with publisher URL/DOI, exact release, raw SHA-256, bytes/rows/schema, survey license, expected coordinate role and independent review record. Unknown/reconstructed records remain excluded; a mere Dropbox metadata hash is NOT a raw SHA-256.
2. Checkout/fetch immutable raw content only at a pinned release, e.g. genuinely uploaded Git LFS with verified object and bytes; compare local raw digest against **reviewed committed manifest**, verify exact provider schema, nulls and counts. Never fetch a mutable live endpoint during production build and silently treat it as frozen.
3. Recreate normalized UTF-8 ICRS source_id,ra_deg,dec_deg with pinned converter/config, *no silent missingness dropping*, unique ID/duplicate policy and frozen deterministic sampling (up to 2,000 points); save full excluded-source accounting and selected ID digest. Sample selection must not depend on outcomes or favorite sky locations.
4. Compare derived bytes SHA-256 to independently reviewed committed derived digest. Require reproducible second-run identical bytes (or explicitly accepted numerical tolerance plus fixed serialization); upload only genuine verified LFS data objects. On mismatches, missing source or bad licence: **fail build** and publish no points, with failure artifact.
5. Version a generated read-only sky index/snapshot with dataset ID, provenance and overlay digests, signed review attribution and display eligibility. Tie to **actual canonical registry** data_provenance + dataset IDs. Reject status aliases or anonymous/new IDs. GitHub branch protection must require this CI gate before merge/deploy.
6. At runtime list only manifest-approved **display** datasets. Fetch exact same-origin immutable path (or validated versioned signed endpoint); WebCrypto verify data bytes against committed immutable digest before drawing Aladin sources. Do not require user CSV or user-entered digest for that mode; keep the current local inspector as separately labeled optional mode. On mismatch/network error/unverified source, render zero markers and a visible diagnostic.
7. UI state must report separately (a) VERIFIED RAW BYTES, (b) REVIEWED UPSTREAM PROVENANCE, (c) APPROVED OBSERVATIONAL DISPLAY, (d) CONTROLLED SCIENTIFIC SUPPORT for specific Claim_ID + Experiment_ID + original/independent manifests, (e) PHYSICAL SUPPORT. No controlled-support badge is possible merely because (a)-(c) hold.
8. Browser/security tests: missing/changed manifest, wrong SHA, absent LFS, unknown registry ID, unverified provenance, unauthorized status promotion, duplicate IDs/coords, RA wrap/poles, fallback source selection, large list pagination/2k cap, external CDS outage, accessibility, CSP/SRI/license and provenance presentation. Include real external Aladin integration smoke separately from deterministic mock CI.

### Scientific claim/adjudication gate
A dataset may have provenance VERIFIED and observational display accepted while controlled support remains FALSE. To make Controlled_Support_Eligible=true for any relevant experiment/claim: preregister a hypothesis and its valid null before outcomes; perform the original controlled run and independent rerun; attach immutable manifests, statistical tests, effect sizes, uncertainty and negative findings; obtain external scientific approval; then make a separate audited, namespace-correct claim/evidence registry PR. For A01 the evidence concerns **internal arithmetic rank coherence**, not a mapping to galaxy positions. A sky overlay alone never proves ACSC, GLMPCT or physical cosmology.

## 5. Expired upload and source recovery inventory
Some earlier ChatGPT conversation attachments are reported expired by the attachment service. That is an attachment-session availability fact, **not a deletion claim** about Dropbox or GitHub. The assistant cannot renew old ChatGPT attachment IDs or recreate missing bytes from search snippets. Do not say they have been re-uploaded.

Live Dropbox evidence identifies:
- STAR_Research_Charter_v0-2.pdf: /STAR/STAR_Research_Charter_v0-2.pdf and an audit-era copy under /star_provenance_r&d/_audit_2026-10-08/repo/charter/; canonical repo already contains charter/STAR_Research_Charter_v0-2.pdf. Same filename/size is insufficient for byte equality without digest comparison.
- SDSSDR18_200000.csv: /STAR/SDSSDR18_200000.csv, 33,007,497 bytes, and /STAR/Documents/STAR/ copy. Historical selected genuine LFS object at data/intake/recovered/2026-10-08/9dca2008683fde4b0f7a90af5de85ee846a30a47f6f6fae3968c83dea06fa5d2.csv is already recorded with SHA-256 but is **not validated upstream as an observational dataset**. Its raw CasJobs export binding still needs review.
- Original manuscript/ECC/criteria PDF-name matches survive in the archived /star_provenance_r&d tree and/or repository docs/ and web_tool/attachments/. Name matching and unequal-sized manuscript variants do not prove that the expired ChatGPT attachment is the same revision. Locate specific target, compare bytes and canonical hash before any replacement or LFS ingestion.
- ALFALFA VizieR raw table has **not** been acquired into verified canonical source storage; PR #68 contains a template only.

Recovery protocol: inventory attachment identity -> locate upstream or Dropbox backup -> retrieve **actual bytes** to a controlled host -> compare SHA-256 with an independently documented original if available -> preserve both versions on mismatch -> submit to a review-only intake with genuine LFS upload if needed -> verify LFS smudge/object -> register provenance without support promotion. A link/metadata receipt is not re-upload. The exact ChatGPT-side attachment must be reattached by its holder if it is needed in this conversation.

## 6. Proposed merge/release sequence
1. Independent reviewers sign #62 and #63 design/theory scope; merge #62 then review/merge stacked #65; do not activate A03.
2. Review #66 observational fixtures independently; merge only as fail-closed diagnostics, not as data acceptance.
3. Audit the **combined** branch after those merges, then approve and merge #64 only with exact source-locked CI, two-flag transition and Issue #67 release approval. No full controlled run in CI preflight.
4. Review #68 web semantics/live CDS; merge as explicitly **local user-hash inspector only**, or supersede in a new PR with genuine CI manifest gating. Do not display verified provenance or scientific support that does not exist.
5. Acquire, version and review a genuine VizieR ALFALFA α.100 corrected table2 source (published 31,502 rows), preserving both radio-centroid and optical-counterpart roles. Follow independent provenance gate, then CI-frozen overlay release.
6. After original controlled experiments and independent replications, review any claim-specific support transitions as independent PRs. Retain all negative results.

## 7. References reviewed
- Governing PDF: charter/STAR_Research_Charter_v0-2.pdf and summary charter/RESEARCH_CHARTER_v0.2.md.
- Canonical registries: registry/dataset_registry_v0.1.csv, data_provenance_registry_v0.1.csv, experiment_registry_v0.2.csv, claim_evidence_v0.2.csv.
- [Issue #67](https://github.com/LcosmosS/S.T.A.R.-Labs/issues/67), PRs #62-#66, #68, their changed file lists, heads and CI checks dated above.
- [VizieR corrected ALFALFA α.100 table2](https://vizier.cds.unistra.fr/viz-bin/VizieR-3?-source=J%2FApJ%2F861%2F49%2Ftable2); Haynes et al., 2018, DOI [10.3847/1538-4357/aac956](https://doi.org/10.3847/1538-4357/aac956).
- [ALFALFA-SDSS Galaxy Catalog](https://doi.org/10.3847/1538-3881/abc018), published cross-survey association example. Not a drop-in independent null or guaranteed match truth.
- [Official Aladin Lite API](https://aladin.cds.unistra.fr/AladinLite/doc/API/); [version-pinning guidance](https://github.com/cds-astro/aladin-lite/blob/master/README.md).
