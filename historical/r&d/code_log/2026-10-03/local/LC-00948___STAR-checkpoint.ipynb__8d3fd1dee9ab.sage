import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import ks_2samp
from pathlib import Path

SYNTHETIC_FILE = "synthetic_cosmos_final/synthetic_cosmic_catalog_final.csv"
REAL_FILE1 = "JApJ94494_2MASS_GAIADR3_EPOCH.csv"
REAL_FILE2 = "DESIDR8_SDSSDR16_SIMBAD.csv"

CHUNK_SIZE = int(50000)

print("🔄 Loading synthetic catalog...")
synth = pd.read_csv(SYNTHETIC_FILE)
print(f"   Synthetic galaxies: {len(synth):,} | Ranks: {sorted(synth['exact_rank'].unique())}")

print("\n🔄 Loading real files (chunked)...")
real1 = pd.concat([chunk for chunk in pd.read_csv(REAL_FILE1, chunksize=CHUNK_SIZE, low_memory=False)], ignore_index=True)
real2 = pd.concat([chunk for chunk in pd.read_csv(REAL_FILE2, chunksize=CHUNK_SIZE, low_memory=False)], ignore_index=True)

print(f"   Real1 (JApJ): {len(real1):,} rows")
print(f"   Real2 (DESI/SDSS): {len(real2):,} rows")

# ────── Key Comparisons ──────
print("\n📊 COMPARISON SUMMARY")

print(f"   Synthetic z (velocity proxy) mean/std : {synth['synthetic_z'].mean():.4f} ± {synth['synthetic_z'].std():.4f}")
print(f"   Real1 Vcmb mean/std                    : {real1['Vcmb'].mean():.1f} ± {real1['Vcmb'].std():.1f} km/s")
print(f"   Real2 zphot mean/std                   : {real2['zphot'].mean():.4f} ± {real2['zphot'].std():.4f}")

print(f"\n   Synthetic RA range : {synth['synthetic_RA'].min():.1f} to {synth['synthetic_RA'].max():.1f}")
print(f"   Real1 RAJ2000 range: {real1['RAJ2000'].min():.1f} to {real1['RAJ2000'].max():.1f}")

# KS-test (fixed with plain int)
print("\nKS-test (synthetic V_comove vs real DM proxy):")
sample_size = 5000
ks_v = ks_2samp(
    synth['V_comove'].sample(int(sample_size), random_state=int(42)),
    real1['DM'].dropna().sample(int(sample_size), random_state=int(42)) * 100   # rough scaling to match order of magnitude
)
print(f"   statistic = {ks_v.statistic:.4f} | p-value = {ks_v.pvalue:.4f}  ← (higher p = better match)")

print("\nSynthetic rank distribution:")
print(synth['exact_rank'].value_counts().sort_index())

# ────── Quick visual comparison ──────
fig, axs = plt.subplots(1, 3, figsize=(15, 4))

synth['synthetic_z'].hist(bins=50, ax=axs[0], alpha=0.7, label='Synthetic z', density=True)
real2['zphot'].hist(bins=50, ax=axs[0], alpha=0.7, label='Real zphot', density=True)
axs[0].set_title('Redshift / velocity proxy')
axs[0].legend()

synth['V_comove'].hist(bins=50, ax=axs[1], alpha=0.7, label='Synthetic V_comove', density=True)
(real1['DM'] * 100).dropna().hist(bins=50, ax=axs[1], alpha=0.7, label='Real DM ×100', density=True)
axs[1].set_title('Comoving volume proxy')
axs[1].legend()

synth['rho_scale'].hist(bins=50, ax=axs[2], alpha=0.7, label='Synthetic rho_scale', density=True)
axs[2].set_title('Density scale')
axs[2].legend()

plt.tight_layout()
plt.show()

print("\n✅ Comparison finished!")
print("   The synthetic catalog now exists and can be directly compared to your real data.")
print("   Next step available: reply with **step 3** for full ML + Entropy Cohomology on both datasets.")