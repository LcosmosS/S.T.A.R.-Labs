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
