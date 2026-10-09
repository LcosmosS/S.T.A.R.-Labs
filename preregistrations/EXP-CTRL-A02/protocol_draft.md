# EXP-CTRL-A02 — prospective leakage-control design; NOT YET PREREGISTERED

Canonical qualified identity `REPO-CSV-v0.2:EXP-CTRL-A02`, `DATA-PROVENANCE-ALL`, `PAR-LEAK-001`, `NULL-LEAK-001`. Do not alias it to the separate STAR-PDF identifier. Canonical status remains **planned**.

## Why this precedes SFR modeling

Historical scripts build `log_SFR_Ha_raw` from the same H-alpha flux/redshift as `log_SFR_Ha`, then use the raw form as a predictor; they also globally fit imputation/scaling and global quantiles before training/test partition. Historical R² and reported fold errors cannot be treated as independent scientific confirmation. This study audits contamination; it must **not** repeat leakage to obtain a strong score.

## Candidate comparisons (not a finalized hypothesis test)

- Hash and register *one* complete raw input source and the target derivation; select target `log_SFR_Ha` or another primary target prospectively, not after viewing residuals.
- Freeze a list of all direct, algebraic or catalog-derived target proxies; blacklist from candidate features. Train imputation, scaling, derived binning, and any supervised selection **inside training folds only**.
- Use group/sky-tile held-out folds when galaxies share observations; preserve the grouping key, missingness and relevant redshift/mass distributions.
- Predeclare (a) ordinary non-arithmetic astrophysical baseline; (b) rank/arithmetic addition with an independently justified galaxy-to-arithmetic association; (c) a leakage-positive control **solely as a diagnostic**, never as evidence of predictive power.
- A candidate statistical null could permute *only the incremental arithmetic predictors* within redshift/mass/sky groups while keeping the target and astrophysical baseline fixed; residual/confounding diagnostics are prerequisites.

## Blocking gates

No final survey sample and source release/sha, allowed features, target ownership, group split, hyperparameter search budget or valid independent arithmetic correspondence is bound to `DATA-PROVENANCE-ALL`. Consequently **`PAR-LEAK-001` and `NULL-LEAK-001` must remain not-preregistered** and the experiment must remain planned. Distinguish a diagnostic leakage audit from the future `EXP-SFR-A01` claim of incremental SFR prediction.

**Current flags:** execution=false, controlled support=false, physical support=false. No model or result was executed. The historical reported MSE and R² remain unreplicated.
