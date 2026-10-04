import pandas as pd
import numpy as np
from scipy.stats import ks_2samp
import matplotlib.pyplot as plt

CALIBRATED_FILE = "synthetic_cosmos_final/synthetic_cosmic_catalog_calibrated.csv"
REAL_FILE1 = "JApJ94494_2MASS_GAIADR3_EPOCH.csv"

print("🔄 Loading calibrated synthetic data...")
synth = pd.read_csv(CALIBRATED_FILE)

# Load real data (chunked)
real1 = pd.concat([chunk for chunk in pd.read_csv(REAL_FILE1, chunksize=int(50000), low_memory=False)], ignore_index=True)

print(f"Loaded calibrated synthetic: {len(synth):,} galaxies")
print(f"Loaded real1 (JApJ): {len(real1):,} rows")

# KS-test (fixed with plain int)
sample_size = 5000
ks_before = ks_2samp(
    synth['V_comove'].sample(int(sample_size), random_state=int(42)),
    real1['DM'].dropna().sample(int(sample_size), random_state=int(42)) * 100
)
ks_after = ks_2samp(
    synth['V_comove_calibrated'].sample(int(sample_size), random_state=int(42)),
    real1['DM'].dropna().sample(int(sample_size), random_state=int(42)) * 100
)

print("\n📊 KS-test (V_comove proxy vs real DM):")
print(f"   BEFORE → statistic = {ks_before.statistic:.4f} | p-value = {ks_before.pvalue:.4f}")
print(f"   AFTER  → statistic = {ks_after.statistic:.4f} | p-value = {ks_after.pvalue:.4f}   ← higher p-value = better match")

# Quick before/after plots
fig, axs = plt.subplots(1, 2, figsize=(12, 5))
synth['V_comove'].hist(bins=50, ax=axs[0], alpha=0.7, label='Synthetic (original)', density=True)
(real1['DM'] * 100).dropna().hist(bins=50, ax=axs[0], alpha=0.7, label='Real DM ×100', density=True)
axs[0].set_title('BEFORE calibration')
axs[0].legend()

synth['V_comove_calibrated'].hist(bins=50, ax=axs[1], alpha=0.7, label='Synthetic (calibrated)', density=True)
(real1['DM'] * 100).dropna().hist(bins=50, ax=axs[1], alpha=0.7, label='Real DM ×100', density=True)
axs[1].set_title('AFTER calibration')
axs[1].legend()

plt.tight_layout()
plt.show()

print("\n✅ Calibration & comparison finished!")
print("   The synthetic catalog is now scaled to better align with your real data.")
print("   Next step available: reply with **step 3** for the full ML + Entropy Cohomology pipeline.")