# EXP-MAP-A03 — prospective MCJ arithmetic mapping preregistration v1

**Qualified ID:** `REPO-CSV-v0.2:EXP-MAP-A03` (not the similarly named broader STAR-PDF comparison). **Status:** protocol prospectively specified and locked in this review branch; canonical `experiment_registry_v0.2.csv` remains **planned** until a separate explicit lifecycle-transition PR satisfies the frozen-audit validator. This is not an executed result or a completed execution-spec binding.

## Narrow scientific question

Does the **rank-blind** map from conductor and exact rational modular `j(E)` induce local arithmetic-rank coherence beyond what a within-conductor-decile rank permutation produces? This is an **internal arithmetic null test**. No astronomical observations enter, and positive results **cannot** establish an arithmetic–cosmic correspondence.

This selects the historical `PAR-MAP-003` (MCJ) candidate, not `PAR-MAP-002` (PTD) or `PAR-MAP-001` (A01). Choices not present in historical R&D are **new prospective decisions**, not retroactively recovered historical defaults. `NULL-MAP-003` was a placeholder; the rule below is proposed for its prospective locked successor.

## Fixed input and cohort

Reuse the *already pinned* `DATA-ARITHMETIC` ecdata input from A01 (SHA-256 `259f3846329395b371e8079c77a6f1097adaebc98a054974573e241416efa968`, gitlink `25cec5ecfec8b9f016eb1631ac633194c2bed39f`, 64,687 source rows). Select exactly curve number 1 per isogeny class: 38,042 representatives. No outcome-based trimming, rank imputation, torsion-derived filtering or replacement is allowed. Recompute `Delta` and `c4` exactly from the integral Weierstrass invariants. Define rational `j=c4³/Delta`.

**Predefined singularity rule:** for `j=0`, `log j` is undefined, so exclude those records deterministically **before inspecting ranks**; publish the complete excluded-label list and count. A zero discriminant, duplicate ID, invalid source hash, nonfinite coordinate or unexpected source/cohort count aborts. This explicitly differs from A01's no-exclusion cohort, and any comparisons must report that difference. No curve or label selection based on test statistic or significance.

## Locked PAR-MAP-003 projection (rank-blind)

For each eligible curve in ascending `(conductor, Cremona-label ASCII)` order, define the 3-dimensional dimensionless coordinates

\[
  x=\ln N,\quad y=\operatorname{Re}(\log j)=\ln|j|
  =3\ln|c_4|-\ln|\Delta|,\quad
  z=\operatorname{Im}(\log j)=
  \begin{cases}0,&j>0,\\\pi,&j<0.\end{cases}
\]

using the principal branch (negative real values have argument `+pi`). Exact integers precede binary64 logs and geometry; no sample-derived scaling, clipping, optimization, jitter, fitting, or rank input is allowed.

## Single confirmatory endpoint

Construct `k=10` nearest-neighbor graph in `(x,y,z)` Euclidean distance. Enumerate all point-distance ties, including coordinate duplicates; break equal-distance ties by ASCII Cremona label, exclude self, and symmetrize directed edges into unique unordered label pairs. Compute

\[
 T_{\rm obs}= -\frac{1}{|E|}\sum_{\{i,j\}\in E}|r_i-r_j|.
\]

Higher `T` means greater local rank similarity. The rank must not influence graph construction. A missing/empty/ambiguous graph is a **failed attempt**, not a change of radius, `k`, norm or selection.

## Locked NULL-MAP-003 and decision

Sort accepted curves by `(N,label)`; assign ten equal-count conductor-order blocks as `floor(10*i/n)` with zero-based rank-blind row index `i`. In each of **999** sequential null realizations, permute ranks independently inside each block with the A01-specified `splitmix64-fisher-yates-v1` algorithm, but **independent new seed 4103** and one continuing 64-bit RNG stream. Preserve identities, `N`, `j`, graph and the rank multiset inside each block. No null may be skipped or regenerated.

\[
p = \frac{1+\#\{b:T_b\ge T_{\rm obs}\}}{1000}.
\]

This protocol has one one-sided endpoint, `alpha=0.005`, no researcher-adjusted hyperparameters. The stricter threshold avoids describing two related preregistered mapping checks as an uncorrected exploratory family, but it **does not change A01's locked alpha=0.01**. Report the exact p-value, all null draws, rank decile counts, `T_obs-median(T_null)`, projection, graph edge count and selected/excluded labels. A conditional-permutation rejection is **internal arithmetic evidence only**.

## Output, stop rules and activation

Write four new, non-overwriting files: `summary.json`, `observed_mcj_projection.csv`, `null_statistics.csv`, `exclusions_j_zero.csv`. Failed checks produce a failure manifest; never silently change cohort, floating-point treatment, RNG or `k`. Report a non-rejection as transparently as a rejection.

No canonical registry rows, source datasets or `EXP-MAP-A01` settings are changed by this document. Separate, reviewable next gates: (1) implement validated MCJ j/sign, tie-handling and RNG fixtures; (2) commit source code and controlled-execution spec; (3) explicitly reconcile audit snapshot and registry status/parameter/null records; (4) run preflight before **separate** execution eligibility activation; (5) conduct independent transaction-bound rerun; (6) consider any controlled-support promotion only after review. Physical support remains false under either inferential outcome.

Locked machine-readable decisions: [config.json](config.json). Baseline A01: [protocol](../EXP-MAP-A01/protocol.md).
