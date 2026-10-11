# EXP-MAP-A01 — preregistration, activation and reproducibility package v0.1

**Type:** read-only review/reproducibility package, assembled against canonical `main` `7f1a03692539542e23b78263422f3be71da952ea`.
**Authority:** [`STAR_Research_Charter_v0-2.pdf`](../../charter/STAR_Research_Charter_v0-2.pdf), SHA-256 `9a63284900d5349f1d307160929b2542885e4c751439b785369b722d349a5c03`.
**Scientific scope:** one preregistered arithmetic rank-permutation null test, not BSD proof, ACSC physical support, a cosmological prediction, SFR modeling, or a mathematical theorem.

## Canonical state (do not overwrite historical files)

- **Preregistered:** `REPO-CSV-v0.2:EXP-MAP-A01`, claim `CLAIM-ACSC-001`, dataset `DATA-ARITHMETIC`, parameters `PAR-MAP-001`, null `NULL-MAP-001`; protocol `EXP-MAP-A01-prereg-v1`.
- **Approved activation:** [PR #78](https://github.com/LcosmosS/S.T.A.R.-Labs/pull/78), approved by an off-author reviewer on its final diff and merged as [`7f1a036`](https://github.com/LcosmosS/S.T.A.R.-Labs/commit/7f1a03692539542e23b78263422f3be71da952ea). Both A01 and `DATA-ARITHMETIC` controlled-execution flags are true on this baseline. The activation is already recorded; this package does not recreate or confer that approval.
- **Shared dataset:** A03 is separately preregistered and remains execution-ineligible. [Compatibility PR #87](https://github.com/LcosmosS/S.T.A.R.-Labs/pull/87) preserves the original A03 dataset row hash and proves the permitted A01-only eligibility-bit transition.
- **Support:** all relevant controlled/physical support flags remain false. A permitted original run is not itself an accepted or independently replicated scientific result.
- **Historical apparent contradiction:** the October 4 `preregistrations/EXP-MAP-A01/dataset_manifest.json` and protocol say execution was disabled *at the time of preregistration*. Preserve those frozen bytes. Current operational authorization resides in the reviewed merged registry transition, not a rewrite of preregistration history. The PR #78 decision docket also retains pre-merge language.

## Frozen primary scientific specification

Upstream [`JohnCremona/ecdata`](https://github.com/JohnCremona/ecdata), commit `25cec5ecfec8b9f016eb1631ac633194c2bed39f`, `allcurves.00000-09999` SHA-256 `259f3846329395b371e8079c77a6f1097adaebc98a054974573e241416efa968`, 2,146,401 bytes, 64,687 source rows. Select **curve number 1 per isogeny class**, yielding **38,042** representatives; no post-hoc filtering.

Primary embedding: longitude = `360 ln(|Delta|)/ln(10^30)`, latitude = `180 ln(N)/ln(10^9)`, elevation = `200 rank`. Compute the unique undirected `k=10` Euclidean base-neighbor graph with ASCII label tie-breaking and use `T=-mean(|elevation_i-elevation_j|)`. Larger `T` indicates more local rank coherence. Regulator is not used.

Null: **999** global rank permutations with one continuous `splitmix64-fisher-yates-v1` state, seed **1729**, fixed curve identities/discriminants/conductors/base graph and rank multiset. Infer `p=(1+count(T_null >= T_obs))/1000`, reject the specified null only when `p<0.01`. There is one preregistered endpoint; no retrospectively selected alternative mapping or interpretation.

Authoritative source files: [`protocol.md`](../../preregistrations/EXP-MAP-A01/protocol.md), [`config.json`](../../preregistrations/EXP-MAP-A01/config.json), [`dataset_manifest.json`](../../preregistrations/EXP-MAP-A01/dataset_manifest.json), [`execution spec`](../../controlled_execution/specs/EXP-MAP-A01.json). This package references these files rather than copying a divergent scientific definition.

## Contents and verification

- [`SOURCE_MANIFEST.json`](SOURCE_MANIFEST.json): immutable source, exact source/row bindings, PR approval, merge and CI lineage.
- [`ACTIVATION_LINEAGE.md`](ACTIVATION_LINEAGE.md): human-readable governance history and A01/A03 coexistence.
- [`REPRODUCE.md`](REPRODUCE.md): two-person original run and independent rerun handoff, hashes and admissible outcomes.
- [`REVIEW_CHECKLIST.md`](REVIEW_CHECKLIST.md): reviewer acceptance and nonclaims.
- [`scripts/verify_exp_map_a01_release_package.py`](../../scripts/verify_exp_map_a01_release_package.py): read-only registry, source and hash verifier; [`tests`](../../tests/test_exp_map_a01_release_package.py); [source-receipt CI](../../.github/workflows/a01_release_package.yml).

From the repository root, with the specified ecdata gitlink initialized and source hydrated:

```sh
python scripts/verify_exp_map_a01_release_package.py --require-source --receipt /tmp/a01-package-read-only.json
python -m unittest discover -s tests -p test_exp_map_a01_release_package.py -v
```

Both commands **must not** invoke the registered A01 statistic, 999-permutation distribution, or production runner. Their PASS is source/software readiness evidence, **not** experimental reproduction. A failed check blocks use of this package; do not edit frozen values merely to obtain PASS.

## Evidence boundaries

The source verifier and the [merged activation CI](https://github.com/LcosmosS/S.T.A.R.-Labs/actions/runs/38098877617) do not contain an original investigator-A controlled result or a separate investigator-B manifest. No p-value, effect size, null distribution, independent replication or ACSC physical inference is claimed by this package. Follow the reproduction runbook only as a **separate accountable controlled transaction**, never in this PR or CI.

Public release, GitHub approval, a DOI, numerical agreement or CI success must not automatically change `Controlled_Support_Eligible` or `Physical_Support_Eligible`. Charter §§12–15, 17, 28–31 govern nulls, parameter locking, negative outcomes, independent validation and reproducibility.
