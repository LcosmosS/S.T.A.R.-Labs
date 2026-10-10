# EXP-MAP-A01 — rebuilt execution-only activation proposal (after PR #77)

Main remains **inactive** until this separate activation PR is approved and merged. The scientific protocol `EXP-MAP-A01-prereg-v1` is not modified.

Exactly two operational booleans become true: `EXP-MAP-A01.Controlled_Execution_Eligible` and `DATA-ARITHMETIC.Controlled_Execution_Eligible`. No claim, cohort, constant, mapping, endpoint, alpha, null, random seed, source hash, code input or output contract changes. The runner spec's two dependent record hashes are mechanically recalculated. All controlled and physical support flags remain false.

## Mandatory proof of source identity and software readiness

Merge ONLY if the dedicated Actions job fully succeeds: verify the repository `ecdata` gitlink is `25cec5ecfec8b9f016eb1631ac633194c2bed39f`; download `allcurves.00000-09999` from that exact upstream commit; verify SHA-256 `259f3846329395b371e8079c77a6f1097adaebc98a054974573e241416efa968`, 64,687 source rows, 38,042 representative records through protocol/tests, audited registry and runner bindings, clean tree and actual `star-controlled-experiment preflight`.

The legacy frozen October audit remains immutable; its validator has a narrow explicit A01 activation exception. No historical status is rewritten, and support promotion is prohibited.

## After activation merge — not in Actions preflight

The first controlled run must use `star-controlled-experiment run --spec controlled_execution/specs/EXP-MAP-A01.json --executor-id investigator-A` on a clean checkout, with a fresh run directory. Preserve null and negative outcomes, including `p>=0.01`. Perform a second transaction-bound rerun from an independent environment/executor via the runner's `rerun` command and `verify-reproduction`. Record the original and independent manifests and SHA-256 sidecars. Do not claim cosmological or physical support from arithmetic-only rank coherence. `Controlled_Support_Eligible` and `Physical_Support_Eligible` remain false until separate scientific review.

 
## Historical reversal and rebuilt authorization gate

Original [PR #64](https://github.com/LcosmosS/S.T.A.R.-Labs/pull/64) was merged without the formal independent human approval demanded by its own activation decision. [PR #77](https://github.com/LcosmosS/S.T.A.R.-Labs/pull/77) restored both controlled-execution eligibility fields to false on `main` at merge commit `791c423514bd0d10c667c42106e55e41e445f09c`, while preserving [PR #76](https://github.com/LcosmosS/S.T.A.R.-Labs/pull/76)'s sky-release selector and browser hash verification. This new PR is a distinct proposal, not a reopened approval or an executed A01 experiment.

**Scientific status:** preregistered, zero original controlled runs, zero independent reproductions, zero controlled/physical support. The 999-permutation endpoint, locked source, null, seed, definitions, cohort, and output contract are unchanged. Do not run `star-controlled-experiment run` on this PR or interpret readiness/preflight as a scientific result.

## Approval required before merge

- A reviewer independent of the author must submit an accountable GitHub **APPROVED** review of this **exact final commit/diff**. An automation review, author comment, or successful preflight alone does not satisfy this requirement.
- Verify the *only operational status transitions* are `EXP-MAP-A01.Controlled_Execution_Eligible` and `DATA-ARITHMETIC.Controlled_Execution_Eligible`, false to true; all controlled-support and physical-support flags remain false.
- Check the deterministic derived registry row hashes, `controlled_execution/specs/EXP-MAP-A01.json`, and the read-only `web_tool/src/lib/star/registry-snapshot.json` binding. None of this grants a sky-display or observational-data promotion.
- Independently inspect the pinned upstream ecdata gitlink **and initialized HEAD** at `25cec5ecfec8b9f016eb1631ac633194c2bed39f`; SHA-256 of `allcurves.00000-09999` is `259f3846329395b371e8079c77a6f1097adaebc98a054974573e241416efa968`, with 64,687 source rows and 38,042 representative records.
- Re-run exact-head Actions, including `A01 source-locked activation preflight`, tests, registry/claim validators, controlled readiness and `star-controlled-experiment preflight`. No inference or original 999-permutation experiment is allowed in activation CI.
- Confirm the frozen `EXP-MAP-A01-prereg-v1` protocol/config and `PAR-MAP-001` / `NULL-MAP-001` are unchanged, together with all code/data input hashes. No post hoc scientific tuning is permitted.

**Review status:** *pending*. Neither the earlier PR #64 merge nor PR #77 revert provides prospective independent authorization for this newly rebuilt proposal. Keep unmerged until the above review succeeds. Do not fabricate or backdate an approval.

**After authorized merge only:** [Issue #67](https://github.com/LcosmosS/S.T.A.R.-Labs/issues/67) tracks the separate investigator-A original controlled run and investigator-B independent reproduction with manifests and sha256 sidecars. Non-rejection and negative outcomes must remain reportable. Even success is an arithmetic-only mapping diagnostic, not cosmological correspondence or physical support.

## New integration blocker detected against current `main` (2026-10-10)

**Not execution-authorized; do not merge this original activation diff.**
The original #78 head predates the merged A03 preregistration (PR #83) and
observational dataset lineage (PR #84). It currently reports an actual merge
conflict with `main`, so the original full-file registry and web snapshot
versions cannot be used as a conflict-resolution source. A future activation
diff must preserve current main's A03 status, all newer provenance rows,
the dynamic audit validator, and the ALADIN release gate.

There is also a distinct **shared dataset / frozen A03 binding** conflict:

- A01 and A03 both reference `DATA-ARITHMETIC`.
- The proposed A01 transition changes that dataset's execution flag
  `false -> true`, with canonical dataset-row digest
  `1b81e05ab90ce822c7dcbda88bdb206f191f6523fac03fea5ecdf55724de44c2`.
- The already frozen A03 execution spec binds the original dataset-row
  digest `2fe4ab7f5763f39c6cde8392c3f7d8ff1a565e4664ce6e192640b99f3fe146d7`.
- A03's canonical preregistration validator requires the shared dataset
  flag `false`, an exact current registry-binding hash, and a binding-only
  preflight that currently requires both experiment and dataset eligibility
  `false`. All three would break after A01's proposed dataset transition,
  even while A03's own experiment flag remains `false`.

A mere Git conflict resolution, a stale A01-only preflight success, or a
forced acceptance of the new dataset digest is **not** adequate.
Before a successor A01 activation proposal can be merge-eligible, an
independently reviewed, reproducible compatibility design must preserve
A03's execution prohibition **and** give a transparent, hash-locked
transition record for any operational A03 spec-bound dataset-row update.
The original scientific A03 protocol, cohort, parameters, null, and
endpoint cannot be silently changed. Assess compatibility with the
A03 pre-execution verification package in PR #86, including its preserved
local and CI receipts, before final approval.

This blocker is in addition to — not a replacement for — the required
off-author **human APPROVED review** on the prospective *exact final*
activation diff. The two execution flags proposed here have no force on
the canonical `main` registry until an authorized merge.
