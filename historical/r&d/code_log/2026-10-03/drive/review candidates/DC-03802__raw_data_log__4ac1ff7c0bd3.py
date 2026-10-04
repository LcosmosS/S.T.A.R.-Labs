print(f"   statistic = {ks_v.statistic:.4f} | p-value = {ks_v.pvalue:.4f}  ← (higher p = better match)")


print("\nSynthetic rank distribution:")
print(synth['exact_rank'].value_counts().sort_index())


# ────── Quick visual comparison ──────
fig, axs = plt.subplots(1, 3, figsize=(15, 4))


synth['synthetic_z'].hist(bins=50, ax=axs[0], alpha=0.7, label='Synthetic z', density=True)
real2['zphot'].hist(bins=50, ax=axs[0], alpha=0.7, label='Real zphot', density=True)
