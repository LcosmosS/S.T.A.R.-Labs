print(f"Loaded calibrated synthetic: {len(synth):,} galaxies")
print(f"Loaded real1 (JApJ): {len(real1):,} rows")


# KS-test (fixed with plain int)
sample_size = 5000
ks_before = ks_2samp(
    synth['V_comove'].sample(int(sample_size), random_state=int(42)),
    real1['DM'].dropna().sample(int(sample_size), random_state=int(42)) * 100
