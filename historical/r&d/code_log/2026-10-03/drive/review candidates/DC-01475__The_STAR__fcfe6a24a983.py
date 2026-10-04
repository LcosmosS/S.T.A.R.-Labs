print(f"Memory usage after feature engineering: {df.memory_usage().sum() / 1024**2:.2f} MB")


# Define final features list =========================================================================================================================================
target = "log_SFR_Ha_raw"
features = [
    "logMass", "Re_kpc", "OH_O3N2_raw", "cosmo_rank",
    "mass_metallicity", "sqrt_Re_kpc", "cosmo_rank_mass", "L_cosmo_s1_mass",
    "log_flux_Ha", "log_flux_Hb", "log_flux_OIII_5007", "log_flux_NII_6584", 
    "log_e_flux_Ha", "L_cosmo_s_0.5", "L_cosmo_s_1.0", "L_cosmo_s_1.5", 
    "L_cosmo_s_2.0", "cluster_density"
]
if all(col in df.columns for col in ['umag', 'gmag', 'rmag', 'imag', 'zmag']):
    features.extend(["color_ug", "color_gr", "color_ri", "color_iz", "e_color_ug", "e_color_gr"])
if all(col in df.columns for col in ['Jmag', 'Kmag']):
    features.extend(["color_JK", "e_color_JK"])
df[new_features] = df[new_features].replace([np.inf, -np.inf], np.nan).fillna(df[new_features].median(skipna=True))


# BSD_likelihood diagnostics ==========================================================================================================================================
print("\nBSD_likelihood Diagnostics:")
print(f"NaN count: {df['BSD_likelihood'].isna().sum()}")
print(f"Mean: {df['BSD_likelihood'].mean():.4f}")
print(f"Median: {df['BSD_likelihood'].median():.4f}")
print(f"Std: {df['BSD_likelihood'].std():.4f}")
print(f"Min: {df['BSD_likelihood'].min():.4f}, Max: {df['BSD_likelihood'].max():.4f}")


plt.figure(figsize=(8, 6))
plt.hist(df['BSD_likelihood'], bins=50, range=(df['BSD_likelihood'].quantile(0.01), df['BSD_likelihood'].quantile(0.99)), density=True, alpha=0.7)
plt.xlabel("BSD_likelihood")
plt.ylabel("Density")
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


# Verify feature availability ============================================================================================================================================================
