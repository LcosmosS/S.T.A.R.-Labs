# A01 activation — independent review of PR #78

**Reviewed PR:** [#78](https://github.com/LcosmosS/S.T.A.R.-Labs/pull/78), head `9a4a19f7fa3e45fb21e66d5598161b29cb0416e1`. **This packet does not approve, merge, close or edit that PR.** The recorded review had only an automated COMMENTED submission, no off-author APPROVED review, and two unresolved threads when checked 2026-10-09.

## Concrete remediations on #78 (not this independent research PR)

1. **Mandatory workflow trigger coverage**: remove `pull_request.paths` entirely to prevent silent skipped preflight after a source or runner dependency changes. At minimum include `data/ecdata` gitlink, `src/cli/star_controlled_experiment.py`, `.github/actions/hydrate-audit/**`, `src/control/**`, configs, specs, registries, dependencies and tests. Removing paths is safer than a possibly incomplete enumerated list.
2. **Invalid watched filename:** change `registry/null_model_registry_v0.1.csv` to actual `registry/null_registry_v0.1.csv`. Audit every referenced path before merge.
3. **Immutable action supply chain:** pin `actions/checkout` and `actions/setup-python` to verified full commit SHAs instead of mutable `@v4`, `@v5` tags. Capture SHA review evidence; **do not invent a SHA**. Review how the curl hydration step authenticates the exact source commit and revalidates digest/row count.
4. **Source/registry coupling:** validate exact ecdata gitlink, byte SHA256, 64,687 source rows, 38,042 representatives, inline config equality, both gate toggles, the runner spec and all derived hashes at one reviewed commit. Positive preflight must never execute the 999 science permutations.
5. **Human governance:** obtain independent human `APPROVED` on the final diff and resolve both review threads. Enforce require-PR, required checks, required independent approval and restrict bypass in repository ruleset before merging. Automated comments and a self-review do **not** count.
6. **Two-flag-only activation:** `EXP-MAP-A01.Controlled_Execution_Eligible` and `DATA-ARITHMETIC.Controlled_Execution_Eligible` may change only in that separate authorized activation. All support flags stay false.

## Gate disposition

**Not approved / not executed / no scientific finding.** This is a review memo, not an alternative activation route. A new research PR cannot make #78's exact final diff reviewed by an independent human. After approval and merge, capture the merge commit and controlled-run manifest and proceed under the existing runner contract, not an improvised script.
