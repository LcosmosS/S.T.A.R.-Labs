plt.title("Distribution of BSD_likelihood")
plt.savefig("BSD_likelihood_histogram.png", dpi=150)
plt.close()

if 'log_SFR_Ha_raw' in df.columns:
    mask = df['BSD_likelihood'].notna() & df['log_SFR_Ha_raw'].notna()
    plt.figure(figsize=(8, 6))
    plt.scatter(df.loc[mask, 'BSD_likelihood'], df.loc[mask, 'log_SFR_Ha_raw'], alpha=0.5, s=10)
    plt.xlabel("BSD_likelihood")
    plt.ylabel("log_SFR_Ha_raw")
    plt.title("BSD_likelihood vs log_SFR_Ha_raw")
    plt.savefig("BSD_likelihood_vs_SFR.png", dpi=150)
    plt.close()

# Verify feature availability
========================================================================
========================================================================
============
missing_features = [f for f in features if f not in df.columns]
if missing_features:
    print(f"Warning: Missing features: {missing_features}")

# Save final dataset
========================================================================
========================================================================
=====================
df.to_csv("*STAR_dataset.csv", index=False)
print("Saved to *STAR_dataset.csv")

# Post-processing diagnostics
========================================================================
========================================================================
============
key_features = [
    'log_SFR_Ha_raw', 'log_Mass_gas', 'Re_kpc', 'flux_Ha', 'cosmo_rank', 'cluster_density',
'OH_O3N2_raw',
    'L_cosmo_s_0.5', 'L_cosmo_s_1.0', 'L_cosmo_s_1.5', 'L_cosmo_s_2.0',  # Add L_cosmo_s_*
