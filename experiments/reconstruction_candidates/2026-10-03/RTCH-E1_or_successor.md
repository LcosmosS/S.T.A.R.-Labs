# RTCH-E1 or successor — version-pinned reconstruction

Date: 2026-10-03. Status: reconstruction candidate; earlier runs remain quarantined synthetic demonstrations.
RTCH-E1 is a noncanonical local experiment, not an alias of `STAR-PDF-v0.2:EXP-RTCH-B01`.

## Goal and evidence

Produce one version-pinned computational experiment with adequate null models, effect sizes and a clean separation from the earlier 900-point and 350-point torus demonstrations. Reference E-LCL-007 through E-LCL-011 in the canonical audit package and the preserved generations in `data/quarantine/2026-10-03_audit/rtch_e1_synthetic/`.

The audit found incompatible implementation generations, underpowered/failed null tests, invalid NaN-derived significance, global representation construction before cross-validation and repeated whole-sample stability rows. The 350-point run's two null replicates cannot resolve corrected permutation significance below 1/3. Neither torus generation tests a cosmic-data correspondence or validates RTCH field equations.

## Reconstruction protocol

1. Register a successor ID or a fully versioned RTCH-E1 revision. Pin code commit/hash, environment, mapping, filtration, point-cloud representation, input hashes, parameters, seeds and repository-relative paths. Resolve the nested manifest's ambiguous input locator.
2. Treat torus inputs as explicitly synthetic positive controls for software behavior. Preserve the old outputs. Use independent arithmetic/astronomical inputs for any empirical correspondence test, with source provenance locked first.
3. Reject nonfinite observed/null statistics and constant-input correlations before p-value calculation. Record an undefined statistic as undefined, never as a favorable p-value. Specify `(1 + exceedances)/(1 + valid null replicates)` and the tail/tie rule.
4. Pre-register null families, effect size, uncertainty, primary endpoint and comparison correction. Choose null count using the required p-value resolution and computational/power budget; do not reuse two null draws for alpha=0.01. Report actual valid null counts and the full null ensemble.
5. Refit imputation, scaling, PCA and any learned representation inside training folds for inductive prediction. Explicitly identify transductive analyses. Exclude outcome-defining inputs from independent target prediction; Faltings-height reconstruction is not held-out prediction when Faltings height is in the input representation.
6. Make stability resamples genuinely different. Record sampled indices, perturbation seeds and sample sizes; a cap equal to the entire dataset is not repeated independent robustness testing. Reconcile CSV results with JSON summaries.
7. Validate filtration semantics and distance-matrix usage against known fixtures. Compute H2 when testing cavities; maxdim=1 cannot supply H2 evidence. Persistent H1 is not a direct filament count.

## Acceptance gate and outputs

Complete, reproducible manifests; finite/constant-input checks; consistent summaries; null resolution adequate for the registered decision rule; real perturbation diagnostics; effect sizes and uncertainty; and independent held-out evidence where claimed. A software fixture passing these checks remains synthetic evidence. Mathematical action/variation audits and physical constraints remain separate canonical experiments.
