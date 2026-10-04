# SFR versus stellar-mass baselines

Date: 2026-10-03. Status: reconstruction candidate; no new model performance claimed.

## Goal and evidence

Separate random-feature stellar-mass baselines from true SFR prediction. E-LCL-013 establishes that inspected `model5.py` predicts `logmstar`, not SFR, while its named input lacks that outcome. Related leakage findings E-LCL-010, E-LCL-012, E-DRV-002 and E-DRV-003 require exact executed versions and fold-local reconstruction. E-LCL-014 and `docs/registries/NAMESPACE.md` govern experiment-ID interpretation.

## Reconstruction protocol

1. Register distinct outcome definitions and units: stellar mass (`logmstar`) versus the chosen SFR measurement, for example log H-alpha SFR. Lock catalog release, quality flags, censoring/zero handling and measurement provenance. Fail schema validation if the outcome is absent.
2. Define independent feature allowlists for each task. Exclude the outcome, deterministic outcome transformations, duplicate measurements that expose the target and outcome-derived features before random feature selection. Record selected features and seed. Do not infer actual historical target inclusion solely because an old script sampled all columns.
3. Split by astronomical object/group before fitting preprocessing. Fit imputation, scaling, population summaries, redshift bins and derived features within training folds. Save split IDs; reserve a final independent dataset or locked test population.
4. For SFR, compare ordinary astrophysical, random-feature, arithmetic-only, combined and arithmetic-permuted models with comparable complexity/search budgets. A morphology/redshift `cosmo_rank` feature must be labeled engineered astrophysical information, not elliptic-curve rank.
5. Verify that any proposed L-cosmo feature actually enters the fitted feature matrix and matches its registered mathematical definition. A calculated/plotted statistic absent from model predictors has no measured incremental effect.
6. Report out-of-sample R-squared, RMSE, MAE, uncertainty, calibration and pre-registered extreme-SFR strata. Retain failed/unstable models and shuffled-target controls. Distinguish statistically detectable correspondence from practical predictive value.

## Acceptance gate and outputs

Two clearly labeled benchmark suites with independent schema/outcome definitions, feature-selection records, fold-local pipelines, source/code/environment hashes, null results and held-out metrics. Historical stellar-mass metrics cannot populate SFR evidence fields. Promote evidence only through the Charter and Data Provenance Registry, after reproducibility and independent-validation requirements are met.
