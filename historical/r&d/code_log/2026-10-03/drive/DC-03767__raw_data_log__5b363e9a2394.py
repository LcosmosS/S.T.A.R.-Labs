import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path
from scipy.stats import ks_2samp


SYNTHETIC_FILE = "synthetic_cosmos_final/synthetic_cosmic_catalog_final.csv"
REAL_FILE1 = "JApJ94494_2MASS_GAIADR3_EPOCH.csv"      # 360k rows
REAL_FILE2 = "DESIDR8_SDSSDR16_SIMBAD.csv"            # 575k rows


CHUNK_SIZE = 50000


print("🔄 Loading synthetic catalog...")
synth = pd.read_csv(SYNTHETIC_FILE)
print(f"   Synthetic galaxies: {len(synth):,} | Ranks: {sorted(synth['exact_rank'].unique())}")


# ────── Load real files (chunked for safety) ──────
print("\n🔄 Loading real files (chunked)...")
real1_list = []
for chunk in pd.read_csv(REAL_FILE1, chunksize=CHUNK_SIZE, low_memory=False):
    real1_list.append(chunk)
real1 = pd.concat(real1_list, ignore_index=True)


real2_list = []
for chunk in pd.read_csv(REAL_FILE2, chunksize=CHUNK_SIZE, low_memory=False):
    real2_list.append(chunk)
real2 = pd.concat(real2_list, ignore_index=True)


print(f"   Real1 (JApJ): {len(real1):,} rows")
print(f"   Real2 (DESI/SDSS): {len(real2):,} rows")


# ────── Feature alignment ──────
print("\n📊 Key comparisons:")


# 1. Redshift / velocity proxy
print(f"   Synthetic z mean/std : {synth['synthetic_z'].mean():.4f} ± {synth['synthetic_z'].std():.4f}")
print(f"   Real1 Vcmb mean/std  : {real1['Vcmb'].mean():.1f} ± {real1['Vcmb'].std():.1f} (km/s)")
print(f"   Real2 zphot mean/std : {real2['zphot'].mean():.4f} ± {real2['zphot'].std():.4f}")


# 2. Position (RA/DE) rough check
print(f"   Synthetic RA range   : {synth['synthetic_RA'].min():.1f} to {synth['synthetic_RA'].max():.1f}")
print(f"   Real1 RAJ2000 range  : {real1['RAJ2000'].min():.1f} to {real1['RAJ2000'].max():.1f}")


# 3. Kolmogorov-Smirnov test on scaled parameters (proxy for scaling-law match)
print("\nKS-test (synthetic V_comove vs real distance proxies):")
ks_v = ks_2samp(synth['V_comove'].sample(5000, random_state=42),
                real1['DM'].dropna().sample(5000, random_state=42) * 100)  # rough scaling
print(f"   V_comove vs DM: statistic={ks_v.statistic:.4f}, p-value={ks_v.pvalue:.4f}")


# 4. Rank distribution in synthetic (should match ACSC expectation)
print("\nSynthetic rank distribution:")
print(synth['exact_rank'].value_counts().sort_index())


# ────── Quick plots (optional — comment out if you don't want figures) ──────
fig, axs = plt.subplots(1, 3, figsize=(15, 4))
