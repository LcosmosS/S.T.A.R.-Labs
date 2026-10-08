# EXP-MAP-A01 — proposed execution-only activation (2026-10-08)

Main remains **inactive** until this separate activation PR is approved and merged. The scientific protocol `EXP-MAP-A01-prereg-v1` is not modified.

Exactly two operational booleans become true: `EXP-MAP-A01.Controlled_Execution_Eligible` and `DATA-ARITHMETIC.Controlled_Execution_Eligible`. No claim, cohort, constant, mapping, endpoint, alpha, null, random seed, source hash, code input or output contract changes. The runner spec's two dependent record hashes are mechanically recalculated. All controlled and physical support flags remain false.

## Mandatory proof of source identity and software readiness

Merge ONLY if the dedicated Actions job fully succeeds: checkout `ecdata` at `25cec5ecfec8b9f016eb1631ac633194c2bed39f`; verify `allcurves.00000-09999` SHA-256 `259f3846329395b371e8079c77a6f1097adaebc98a054974573e241416efa968`, 64,687 source rows, 38,042 representative records through protocol/tests, audited registry and runner bindings, clean tree and actual `star-controlled-experiment preflight`.

The legacy frozen October audit remains immutable; its validator has a narrow explicit A01 activation exception. No historical status is rewritten, and support promotion is prohibited.

## After activation merge — not in Actions preflight

The first controlled run must use `star-controlled-experiment run --spec controlled_execution/specs/EXP-MAP-A01.json --executor-id investigator-A` on a clean checkout, with a fresh run directory. Preserve null and negative outcomes, including `p>=0.01`. Perform a second transaction-bound rerun from an independent environment/executor via the runner's `rerun` command and `verify-reproduction`. Record the original and independent manifests and SHA-256 sidecars. Do not claim cosmological or physical support from arithmetic-only rank coherence. `Controlled_Support_Eligible` and `Physical_Support_Eligible` remain false until separate scientific review.


## Independent-review disposition and Issue #67 (2026-10-08)

**Technical assessment only — activation is not approved or executed.** The prior exact-head PR CI snapshot `119d74ec7bde40b5d4f3ea25a2e821f74c3aeac8` reported 7/7 passing workflows, including the *actual* SHA-bound `A01 source-locked activation preflight`. The changed-file audit shows the only two proposed eligibility fields change from `false` to `true`: `EXP-MAP-A01` and `DATA-ARITHMETIC`; the source-identity, scientific protocol, primary statistic, null, seed and all support/physical flags remain unchanged. This is sufficient to regard the **software preactivation checks provisionally complete**, subject to final-head reruns and independent diff assessment. It is **not** the final authorization described in the Research Charter.

As of this docket, GitHub shows **no submitted independent review approval** for [PR #64](https://github.com/LcosmosS/S.T.A.R.-Labs/pull/64) and the PR remains a draft. [Issue #67](https://github.com/LcosmosS/S.T.A.R.-Labs/issues/67) is the *A01 execution/replication checklist*, **not PR #67**, and confers no permission to run. Maintain `Controlled_Execution_Eligible=false` on `main` until independent governance/science signoff and authorized merge. Do not issue a self-approval or create a simulated reviewer decision.

Independent signoff must verify (a) exact-source 64,687/38,042 counts and SHA-256, (b) two-and-only-two flag changes and refreshed dependent binding hashes, (c) no protocol drift relative to frozen A01, (d) preflight green on final head, (e) required branch-protection and reviewer independence. Then mark the PR ready for review and obtain a valid **human/independent formal approval** before merge. The original 999-draw experiment and separate investigator-B reproduction are **subsequent** Issue #67 execution gates, not prerequisites to the code-only activation merge. An approved activation does not establish arithmetic hypothesis support or observational correspondence.

### Multi-PR integration check

The other PRs (#62–#63, #65–#66, #68–#71) are review-only/candidate or observational branches and must not alter A01 source, parameter/null, eligibility or claim-support state accidentally. In particular the committed `web_tool/src/lib/star/registry-snapshot.json` mirrors specific CSV bytes: **after** #64 merges, independently rebase/merge any open web PRs against `main`, regenerate the snapshot using the normal registry synchronization command, and rerun mandatory CI. Never backfill an “independent approval” or controlled-run success by editing a website label.
