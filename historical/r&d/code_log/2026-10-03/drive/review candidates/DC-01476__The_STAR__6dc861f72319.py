if missing_features:
    print(f"Warning: Missing features: {missing_features}")


# Save final dataset =====================================================================================================================================================================
df.to_csv("*STAR_dataset.csv", index=False)
print("Saved to *STAR_dataset.csv")


# Post-processing diagnostics ============================================================================================================================================================
key_features = [
    'log_SFR_Ha_raw', 'log_Mass_gas', 'Re_kpc', 'flux_Ha', 'cosmo_rank', 'cluster_density', 'OH_O3N2_raw',
    'L_cosmo_s_0.5', 'L_cosmo_s_1.0', 'L_cosmo_s_1.5', 'L_cosmo_s_2.0',  # Add L_cosmo_s_* features
    'BSD_likelihood', 'mass_metallicity', 'cosmo_rank_mass', 'L_cosmo_s1_mass',  # Add engineered features
    'log_flux_Ha', 'log_flux_Hb', 'log_flux_OIII_5007', 'log_flux_NII_6584', 'log_e_flux_Ha'  # Add flux/morphology features
]
print("\nPost-processing diagnostics:")
for col in key_features:
    if col in df.columns:
        nan_count = df[col].isna().sum()
        inf_count = np.isinf(df[col]).sum()
        mean_val = df[col].mean()
        median_val = df[col].median()
        std_val = df[col].std()
        min_val = df[col].min()
        max_val = df[col].max()
        sample_vals = df[col].iloc[:5].tolist()
        print(f"{col}: NaN = {nan_count}, Inf = {inf_count}, Mean = {mean_val:.4f}, Median = {median_val:.4f}, "
