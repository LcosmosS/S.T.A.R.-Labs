print("\n📊 KS-test (V_comove proxy vs real DM):")
print(f"   BEFORE → statistic = {ks_before.statistic:.4f} | p-value = {ks_before.pvalue:.4f}")
print(f"   AFTER  → statistic = {ks_after.statistic:.4f} | p-value = {ks_after.pvalue:.4f}   ← higher p-value = better match")


# Quick before/after plots
fig, axs = plt.subplots(1, 2, figsize=(12, 5))
synth['V_comove'].hist(bins=50, ax=axs[0], alpha=0.7, label='Synthetic (original)', density=True)
(real1['DM'] * 100).dropna().hist(bins=50, ax=axs[0], alpha=0.7, label='Real DM ×100', density=True)
