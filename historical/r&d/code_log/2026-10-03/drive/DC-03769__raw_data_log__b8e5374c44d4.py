import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import ks_2samp
from pathlib import Path


SYNTHETIC_FILE = "synthetic_cosmos_final/synthetic_cosmic_catalog_final.csv"
REAL_FILE1 = "JApJ94494_2MASS_GAIADR3_EPOCH.csv"
REAL_FILE2 = "DESIDR8_SDSSDR16_SIMBAD.csv"


CHUNK_SIZE = 50000


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
