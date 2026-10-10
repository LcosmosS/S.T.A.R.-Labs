# Paper II — source-locked arithmetic projection null tests

**Allowed main claim:** Results of a preregistered arithmetic-only projection/rank coherence test on a fixed ecdata corpus, without astrophysical observation or cosmological correspondence.

## Mandatory sequence

1. Source provenance: upstream ecdata commit `25cec5ecfec8b9f016eb1631ac633194c2bed39f`, exact `allcurves.00000-09999` SHA256 `259f3846329395b371e8079c77a6f1097adaebc98a054974573e241416efa968`, source license and complete parsing/row counts.
2. A01 execution authorization: separate reviewed PR, correct preflight dependency coverage and branch protection, clean source/spec check; not just green CI.
3. No alteration of fixed cohort, projection, rank-blind 10NN graph, 999 SplitMix64 permutations, alpha, one-sided statistic or p-rule. Archive graph ties and full null realizations with hashes, plus raw rank/discriminant labels.
4. Reproduce original transaction independently from a clean environment, compare all null statistics/summary/labels and record discrepancies rather than rounding them away.
5. Report either result: `p < 0.01` rejects the *global rank-permutation null*, otherwise do not reject. Report effect size and exact Monte Carlo resolution; do not read `p >= 0.01` as equivalence or zero association.
6. Separately preregister future conditional/permutation successors (such as MCJ A03) with independent source tie/null tests, and apply properly declared multiple-outcome interpretations. Their status is not inherited from A01.
7. Bias and robustness discussion: nonuniform conductor/rank structure, isogeny-class selection, discriminant magnitude, graph degeneracies, unconditional null's limitations and carefully segregated exploratory checks.

**Current evidence:** preregistered protocol/software and verified pinned source; no controlled eligible A01 result or independent human reproduction on baseline. **No p-value, acceptance statement or graph effect size is reported here.**

**Suggested title (provisional):** *Preregistered null-model tests of rank coherence under arithmetic projections of elliptic-curve invariants.*
