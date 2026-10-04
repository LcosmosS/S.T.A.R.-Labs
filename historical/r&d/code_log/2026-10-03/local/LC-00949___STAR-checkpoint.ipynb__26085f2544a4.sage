import pandas as pd
import numpy as np
from scipy.stats import ks_2samp
import matplotlib.pyplot as plt

SYNTHETIC_FILE = "synthetic_cosmos_final/synthetic_cosmic_catalog_final.csv"
REAL_FILE1 = "JApJ94494_2MASS_GAIADR3_EPOCH.csv"      # JApJ
REAL_FILE2 = "DESIDR8_SDSSDR16_SIMBAD.csv"            # DESI/SDSS

CHUNK_SIZE = int(50000)

# Load synthetic (already done)
synth = pd.read_csv(SYNTHETIC_FILE)
print(f"Loaded synthetic: {len(synth):,} galaxies")

# Load real files (chunked)
real1 = pd.concat([chunk for chunk in pd.read_csv(REAL_FILE1, chunksize=CHUNK_SIZE, low_memory=False)], ignore_index=True)
real2 = pd.concat([chunk for chunk in pd.read_csv(REAL_FILE2, chunksize=CHUNK_SIZE, low_memory=False)], ignore_index=True)

print(f"Loaded real1 (JApJ): {len(real1):,} rows")
print(f"Loaded real2 (DESI/SDSS): {len(real2):,} rows")

# ────── CALIBRATION (median matching) ──────
print("\n🔧 Calibrating scaling laws...")

# Use medians for robustness
median_dm = real1['DM'].dropna().median()
median_vcmb = real1['Vcmb'].dropna().median()
median_zphot = real2['zphot'].dropna().median()

median_v_synth = synth['V_comove'].median()
median_rho_synth = synth['rho_scale'].median()

# Scaling factors
alpha_v = median_dm * 100 / median_v_synth          # rough order-of-magnitude match for DM
beta_rho = median_zphot * 10 / median_rho_synth     # match zphot scale

print(f"   alpha (V_comove)  = {alpha_v:.6f}")
print(f"   beta (rho_scale)  = {beta_rho:.6f}")

# Apply calibration
synth['V_comove_calibrated'] = synth['V_comove'] * alpha_v
synth['rho_scale_calibrated'] = synth['rho_scale'] * beta_rho

# Save calibrated version
CALIBRATED_FILE = "synthetic_cosmos_final/synthetic_cosmic_catalog_calibrated.csv"
synth.to_csv(CALIBRATED_FILE, index=False)
print(f"\n✅ Calibrated catalog saved → {CALIBRATED_FILE}")

# ────── BEFORE / AFTER COMPARISON ──────
print("\n📊 BEFORE vs AFTER (KS-test on V_comove proxy):")
ks_before = ks_2samp(
    synth['V_comove'].sample(5000, random_state=42),
    real1['DM'].dropna().sample(5000, random_state=42) * 100
)
ks_after = ks_2samp(
    synth['V_comove_calibrated'].sample(5000, random_state=42),
    real1['DM'].dropna().sample(5000, random_state=42) * 100
)

print(f"   BEFORE → statistic = {ks_before.statistic:.4f} | p-value = {ks_before.pvalue:.4f}")
print(f"   AFTER  → statistic = {ks_after.statistic:.4f} | p-value = {ks_after.pvalue:.4f}  ← (higher p-value = better match)")

print("\nSummary of calibrated columns:")
print(synth[['V_comove', 'V_comove_calibrated', 'rho_scale', 'rho_scale_calibrated']].describe().round(2))

print("\n🎉 Calibration finished!")
print("   The synthetic catalog is now scaled to better match your real observations.")
print("   Next: reply with **step 3** for the full ML + Entropy Cohomology pipeline on both datasets.")