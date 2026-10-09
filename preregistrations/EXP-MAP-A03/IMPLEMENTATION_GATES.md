# EXP-MAP-A03 implementation (fixtures only)

This PR adds exact arithmetic `c4`/discriminant and the principal rational-`j` mapping, explicit j=0 exclusions before rank access, a rank-blind 3D neighbor graph, conditioned conductor deciles, and a **three-draw fixture only**.

**Production has no executable full-cohort entrypoint.** Running the module exits with a deliberate error until the separate canonical transition and activation-review PRs. The 999-draw inferential function is intentionally **not** exposed or run; a controlled runner implementation/spec and pinned source code hashes must be reviewed next.

This branch is stacked on PR #62. When #62 is merged, rebase/retarget here before changing canonical statuses. No historical scores are validated, no inference result exists and all support flags remain false.
