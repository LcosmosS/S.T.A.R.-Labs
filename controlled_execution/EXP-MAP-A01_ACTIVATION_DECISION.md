# EXP-MAP-A01 — proposed execution-only activation (2026-10-08)

Main remains **inactive** until this separate activation PR is approved and merged. The scientific protocol `EXP-MAP-A01-prereg-v1` is not modified.

Exactly two operational booleans become true: `EXP-MAP-A01.Controlled_Execution_Eligible` and `DATA-ARITHMETIC.Controlled_Execution_Eligible`. No claim, cohort, constant, mapping, endpoint, alpha, null, random seed, source hash, code input or output contract changes. The runner spec's two dependent record hashes are mechanically recalculated. All controlled and physical support flags remain false.

## Mandatory proof of source identity and software readiness

Merge ONLY if the dedicated Actions job fully succeeds: checkout `ecdata` at `25cec5ecfec8b9f016eb1631ac633194c2bed39f`; verify `allcurves.00000-09999` SHA-256 `259f3846329395b371e8079c77a6f1097adaebc98a054974573e241416efa968`, 64,687 source rows, 38,042 representative records through protocol/tests, audited registry and runner bindings, clean tree and actual `star-controlled-experiment preflight`.

The legacy frozen October audit remains immutable; its validator has a narrow explicit A01 activation exception. No historical status is rewritten, and support promotion is prohibited.

## After activation merge — not in Actions preflight

The first controlled run must use `star-controlled-experiment run --spec controlled_execution/specs/EXP-MAP-A01.json --executor-id investigator-A` on a clean checkout, with a fresh run directory. Preserve null and negative outcomes, including `p>=0.01`. Perform a second transaction-bound rerun from an independent environment/executor via the runner's `rerun` command and `verify-reproduction`. Record the original and independent manifests and SHA-256 sidecars. Do not claim cosmological or physical support from arithmetic-only rank coherence. `Controlled_Support_Eligible` and `Physical_Support_Eligible` remain false until separate scientific review.
