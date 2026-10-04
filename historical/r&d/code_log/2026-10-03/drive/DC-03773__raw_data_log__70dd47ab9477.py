print(f"   BEFORE → statistic = {ks_before.statistic:.4f} | p-value = {ks_before.pvalue:.4f}")
print(f"   AFTER  → statistic = {ks_after.statistic:.4f} | p-value = {ks_after.pvalue:.4f}  ← (higher p-value = better match)")


print("\nSummary of calibrated columns:")
print(synth[['V_comove', 'V_comove_calibrated', 'rho_scale', 'rho_scale_calibrated']].describe().round(2))


print("\n🎉 Calibration finished!")
print("   The synthetic catalog is now scaled to better match your real observations.")
print("   Next: reply with **step 3** for the full ML + Entropy Cohomology pipeline on both datasets.")
