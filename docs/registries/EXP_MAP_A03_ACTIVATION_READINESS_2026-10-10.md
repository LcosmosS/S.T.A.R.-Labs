# EXP-MAP-A03 activation-readiness and shared-dataset review dossier

**Date:** 2026-10-10. **Baseline main commit:** 76a35aee9c11774ede4d1ff1892c2e6bee959b7d. **Disposition:** ADMINISTRATIVE / PRE-ACTIVATION REVIEW ONLY; do not execute either registered experiment or merge an activation transition as part of this packet.

**Governing authority:** [STAR Research Charter v0.2 PDF](../../charter/STAR_Research_Charter_v0-2.pdf), PDF SHA-256 recorded by the A03 verification report as `9a63284900d5349f1d307160929b2542885e4c751439b785369b722d349a5c03`. Consult the actual PDF before independent approval. Relevant sections identified in the existing A03 review are §§12–15, 17, 23 and 28–31; do not substitute this dossier for the Charter.

## Current state and exact identity

| Gate | State on the inspected main | What is still required |
| --- | --- | --- |
| Frozen A03 preregistration | `EXP-MAP-A03-prereg-v1`, `preregistered` (PR #83) | No redesign; preserve scientific input, output and statistical specification |
| Pre-execution verification | Exact-source and synthetic-reference checks passed (PR #86) | Independent verification evidence is **not** the real-cohort inference |
| Shared dataset compatibility | PR #87 merged an exact **A01-only**, still-inactive-A03 compatibility certificate | Choose future activation order; do not treat the helper as an A03 activation waiver |
| Controlled execution | A01 `false`, A03 `false`, DATA-ARITHMETIC `false` | Separate prospective activation PR, exact-head preflight and off-author human review |
| Controlled support | `false` | Authorized output, independently rerun and reviewed before claim-level promotion |
| Physical support | `false` | New physical mechanism, preregistered blind prediction and independent survey testing |

The [candidate transition ledger](../../registry/preregistration_transition_candidates_v0.1.json) was created 2026-10-08 at its original recorded baseline. Its stale A03 `planned` state has been reconciled to the already-canonical `preregistered` state, with the existing `preregistered_protocol_locked_execution_disabled` label and activation-only next gate. The original ledger creation date and baseline SHA remain historical. **No experiment registry row, controlled spec, parameter/null, code input, executed output, or eligibility flag changes in this PR.** The ledger validator now rejects reverting to the stale planned label.

## Frozen source and analytical contract

- Source: JohnCremona/ecdata gitlink `25cec5ecfec8b9f016eb1631ac633194c2bed39f`, SHA-256 `259f3846329395b371e8079c77a6f1097adaebc98a054974573e241416efa968`. 64,687 rows → 38,042 number-1 representatives → 106 exact `j=0` exclusions → 37,936 A03 accepted curves.
- A03: `CLAIM-ACSC-002`, `DATA-ARITHMETIC`, `PAR-MAP-003`, `NULL-MAP-003`. Principal-branch rank-blind embedding; deterministic Euclidean `k=10` neighbor graph with ASCII tie handling.
- Null: 999 conductor-decile rank permutations, original ranks, continuously advanced SplitMix64–Fisher–Yates seed 4103, one-sided α=0.005; no post-hoc cohort exclusions.
- Frozen output contract: `summary.json`, `observed_mcj_projection.csv`, `null_statistics.csv`, `exclusions_j_zero.csv`. The existing [A03 report](../../research/independent_review/2026-10-16/A03_PREEXECUTION_VERIFICATION.md) and [archival review package](../../release_packages/EXP-MAP-A03-preexecution-verification-v0.1/README.md) are verification evidence, not an execution or approval event.

## The A01/A03 shared DATA-ARITHMETIC transition is NOT general activation

| Record SHA-256 (canonical JSON of full CSV row) | Inactive state | Exact hypothetical A01-only transition |
| --- | --- | --- |
| DATA-ARITHMETIC | `2fe4ab7f5763f39c6cde8392c3f7d8ff1a565e4664ce6e192640b99f3fe146d7` | `1b81e05ab90ce822c7dcbda88bdb206f191f6523fac03fea5ecdf55724de44c2` |
| EXP-MAP-A01 | `31f0137f1de87ba1b548758383b664dab13515205a3c2696b0c0edf573a5f4b3` | `97dac41c4d8a866d0abbcdf5515829328e92ea1fb3cf7b4d03e1d9b9c0b9c868` |
| EXP-MAP-A03 | `3b0bb9c77c80a19a0fca69103f084bb9368593d56d1e3bf037775fb74732794e` | **unchanged / execution=false** |

The [merged design](A01_A03_SHARED_DATASET_COMPATIBILITY_DESIGN_v0.1.md) and [mutation tests](../../tests/test_a01_a03_shared_dataset_compatibility.py) permit the **sole shared dataset execution-bit change for exact A01-only activation**, while A03 remains ineligible. They reverse the changed dataset bit, demand exact frozen A01 and A03 row hashes, reject drift, partial activation and support promotion, and retain closed normal A03 preflight. The original frozen A03 spec still binds the inactive dataset row.

**Important limitation:** A03's *own* experiment flag is still required false by the existing A03 validator and compatibility helper. Therefore PR #87 by itself does NOT allow an A03 activation PR to turn its flag true. The additional hash/validation transition must be separately designed, audited, tested and approved, without silently rewriting the frozen scientific protocol. This is the remaining technical boundary, rather than an unsolved A01-first compatibility issue.

Future activation **ordering is a scientific-governance decision**:

1. **A01-first:** review/repair conflicted PR #78 (or supersede it), activate *only* A01 experiment + DATA-ARITHMETIC dataset, and retain A03 inactive under the PR #87 compatibility certificate. A later distinct A03 activation would need to bind its own eligible experiment-row transition and preserve the original frozen science.
2. **A03-first:** cannot be implemented using the A01-only helper. Because A01's current preregistration validation also expects the dataset flag false, any A03-first plan needs a newly reviewed A01-inactive compatibility design and A03 activation-spec binding transaction. No default A03-first permission exists.

Do not silently update frozen A03 source/parameter/null/config/protocol hashes merely to satisfy a validator. Distinguish operational activation metadata from predeclared scientific design. Preserve the original inactive A03 controlled spec as historical review evidence if an activation-only operational successor is proposed.

## Gate 1: authorized execution only

Before any activation: reconcile this ledger; select the activation sequence; prepare a clean exact-main diff listing the only permitted execution eligibility flips and mechanically derived spec/registry snapshot; verify unchanged scientific hashes and all non-target rows; run full source-locked preflight/CI plus invalid/partial-state mutation tests; and obtain an off-author **human APPROVED** review of the exact final diff. CI must not compute the actual 37,936-curve endpoint or its 999 real nulls. Green automation is not independent scientific authorization.

## Gate 2: controlled arithmetic evidence only

The registered primary endpoint is

\[
T_{\mathrm{obs}}=-\frac{1}{|E|}\sum_{\{i,j\}\in E}|r_i-r_j|.
\]

The exact registered p-value is

\[
p=\frac{1+\#\{b:T_b\ge T_{\mathrm{obs}}\}}{1000},\qquad \alpha=0.005.
\]

**Reject the one-sided null only for p<0.005**; with B=999 this permits **at most 3** null statistics at least as large as the observation (ties count against rejection). Authorized execution would require a write-once hashed original result with all four files, separate investigator rerun and comparison, complete null and effect-size interpretation, a reviewable decision including non-rejection and invalid-run reporting, and a distinct claim-level support approval. A valid null rejection could support only the prespecified scoped arithmetic coherence claim, **not a cosmological or physical correspondence**.

## Gate 3: independent physical hypothesis and validation

A03 has no galaxies, sky coordinates, SFR observables, independent gravitational mechanism or blinded physical target. Any later physical claim needs a separate preregistration deriving a testable observable from an independently justified mechanism, freezing survey selection/matching/masks and baselines, controlling uncertainty and multiple testing, verifying blind/held-out predictions, and replicating across data sources. ALADIN Lite display eligibility is a different approval gate and does not establish physical correspondence. The Charter's statistical correspondence, replication, prediction and theory-success levels must remain distinct.

## Proposed subsequent deliverable and required signoff

This PR is **only** the ledger reconciliation, anti-regression tests and review dossier. No A01 or A03 activation PR is opened or merged by this package. The next separate prospective activation proposal must declare A01-first or A03-first, rederive exact row/spec hashes at its final head, demonstrate compatibility with frozen A01 and A03 protocols and the current observational provenance/ALADIN release gates, pass CI, and obtain a recorded off-author approval. If scientific inputs need substantive revision, stop and preregister a new version and Experiment_ID.

**Non-claims:** no registered endpoint/null run, no independent investigator replication, no authorized execution, no support flags, no physical prediction, no theorem acceptance, and no approved sky release.
