print(f"A_Ha_mw: mean={np.mean(A_Ha_mw):.4f}, std={np.std(A_Ha_mw):.4f}, "
      f"min={np.min(A_Ha_mw):.4f}, max={np.max(A_Ha_mw):.4f}")
if ebv is not None:
    print(f"EBV: mean={np.mean(ebv):.4f}, std={np.std(ebv):.4f}, "
          f"min={np.min(ebv):.4f}, max={np.max(ebv):.4f}")

# Update flux_Ha_corr with extinction correction
========================================================================
============================================================
df['flux_Ha_corr'] = df['flux_Ha'] * 10**(0.4 * (df['A_Ha'] + A_Ha_mw))

# Diagnostics for flux_Ha_corr
========================================================================
========================================================================
======
print(f"flux_Ha_corr: mean={df['flux_Ha_corr'].mean():.4f}, std={df['flux_Ha_corr'].std():.4f}, "