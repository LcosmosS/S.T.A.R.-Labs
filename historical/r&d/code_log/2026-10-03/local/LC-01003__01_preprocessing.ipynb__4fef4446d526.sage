## Next steps
- Run the full TDA pipeline on the saved `acsc_projected_primary_aligned.csv` using `acsc/tda_pipeline.py`.
- Pre-register exact choices for `Amax`, `Nmax`, `V0`, `TOP_SCALE`, quantile transformer details, and null model seeds.
- Run null models (Null-A, Null-B, Null-C) using `acsc/null_models.py` and compute W2 distributions with `acsc/statistics.py`.

## Checklist before main experiment
- [ ] Confirm `COSMIC_FILE` path and selection cuts (volume-limited sample).
- [ ] Pre-register projection parameter values and quantile transformer interpolation method.
- [ ] Save random seeds and software versions (manifest.json).
- [ ] Run ablation tests (remove Wr, remove quantile alignment) and save results.
