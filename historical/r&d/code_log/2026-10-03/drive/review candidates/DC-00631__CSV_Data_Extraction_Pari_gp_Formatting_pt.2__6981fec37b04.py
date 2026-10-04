    # Base SFR with non-linear terms (from polynomial model)
    base_sfr = 4.25 * logmass + 49.04 * z - 0.22 * logmass**2 - 3.94 * logmass * z + 1.30 * z**2
    
    # Quenching term for high-mass galaxies
    quenching_term = -gamma * np.maximum(logmass - mass_threshold, 0)
    
    # Low-mass adjustment
    if logmass < 9.0:
        base_sfr *= low_mass_factor  # Reduce SFR for low-mass galaxies
    
    return base_sfr + quenching_term


# Compute predicted SFR with refined model
df['predicted_sfr'] = df.apply(lambda row: bsd_predicted_sfr(row[logmass_col], row[z_col]), axis=1)


# **Group-Specific Adjustments**
# Bin logmass into quartiles if 'group' not present
if 'group' not in df.columns:
    df['group'] = pd.cut(df[logmass_col], bins=4, labels=['Low', 'Mid-Low', 'Mid-High', 'High'])
    print("Created 'group' column by binning logmass into 4 quartiles.")


# Compute MSE per group
mse_per_group = df.groupby('group').apply(
    lambda x: mean_squared_error(x[sfr_col], x['predicted_sfr'])
)
print("\nMSE per Group (Refined Model):")
print(mse_per_group)


# Plot observed vs. predicted SFR per group
for group in df['group'].unique():
    group_data = df[df['group'] == group]
    plt.scatter(group_data[sfr_col], group_data['predicted_sfr'], alpha=0.5)
    plt.xlabel('Observed SFR')
    plt.ylabel('Predicted SFR')
    plt.title(f'Observed vs. Predicted SFR - {group} (Refined Model)')
    plt.plot([group_data[sfr_col].min(), group_data[sfr_col].max()],
             [group_data[sfr_col].min(), group_data[sfr_col].max()], 'r--')
    plt.savefig(f'observed_vs_predicted_sfr_{group}_refined.png')
    plt.close()
print("Saved group-specific SFR plots (e.g., 'observed_vs_predicted_sfr_Low_refined.png').")


# **Validate with Visuals**
# Residual plots
plt.scatter(df[logmass_col], df[sfr_col] - df['predicted_sfr'], alpha=0.5)
plt.xlabel('Logmass')
plt.ylabel('Residual (Observed - Predicted SFR)')
plt.title('Residuals vs. Logmass (Refined Model)')
plt.savefig('residuals_vs_logmass_refined.png')
plt.close()


plt.scatter(df[z_col], df[sfr_col] - df['predicted_sfr'], alpha=0.5)
plt.xlabel('Redshift (z)')
plt.ylabel('Residual (Observed - Predicted SFR)')
plt.title('Residuals vs. z (Refined Model)')
plt.savefig('residuals_vs_z_refined.png')
plt.close()
print("Saved residual plots ('residuals_vs_logmass_refined.png', 'residuals_vs_z_refined.png').")


# Overall MSE with refined model
mse_refined = mean_squared_error(df[sfr_col], df['predicted_sfr'])
print(f"\nOverall MSE with Refined Model: {mse_refined:.4f}")


print("\nScript completed successfully!")
