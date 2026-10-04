# Handle missing values
imputer = SimpleImputer(strategy='mean') df[[logmass_col, z_col, sfr_col]] = imputer.fit_transform(df[[logmass_col, z_col, sfr_col]])
# Refined SFR prediction function
def bsd_predicted_sfr(logmass, z, mass_threshold=9.0, gamma=0.2, low_mass_factor=0.5): """ Predict SFR with enhanced quenching and mass-specific adjustments. - Non-linear terms: logmass^2, z^2, logmass*z - Quenching: Reduces SFR for high-mass galaxies - Low-mass scaling: Adjusts SFR for logmass < 9 """ # Base SFR with non-linear terms base_sfr = 4.25 * logmass + 49.04 * z - 0.22 * logmass**2 - 3.94 * logmass * z + 1.30 * z**2
# Quenching for high-mass galaxies
quenching_term = -gamma * np.maximum(logmass - mass_threshold, 0)


# Adjust for low-mass galaxies
if logmass < 9.0:
    base_sfr *= low_mass_factor


return base_sfr + quenching_term
# Compute predicted SFR
df['predicted_sfr'] = df.apply(lambda row: bsd_predicted_sfr(row[logmass_col], row[z_col]), axis=1)
# Bin into mass groups
df['group'] = pd.cut(df[logmass_col], bins=4, labels=['Low', 'Mid-Low', 'Mid-High', 'High']) print("Created 'group' column by binning logmass into quartiles.")
# MSE per group
mse_per_group = df.groupby('group').apply( lambda x: mean_squared_error(x[sfr_col], x['predicted_sfr']) ) print("\nMSE per Group:") print(mse_per_group)
# Group-specific SFR plots
for group in df['group'].unique(): group_data = df[df['group'] == group] plt.scatter(group_data[sfr_col], group_data['predicted_sfr'], alpha=0.5) plt.xlabel('Observed SFR') plt.ylabel('Predicted SFR') plt.title(f'Observed vs. Predicted SFR - {group}') plt.plot([group_data[sfr_col].min(), group_data[sfr_col].max()], [group_data[sfr_col].min(), group_data[sfr_col].max()], 'r--') plt.savefig(f'observed_vs_predicted_sfr_{group}.png') plt.close() print("Saved SFR plots (e.g., 'observed_vs_predicted_sfr_Low.png').")
# Residual plots
plt.scatter(df[logmass_col], df[sfr_col] - df['predicted_sfr'], alpha=0.5) plt.xlabel('Logmass') plt.ylabel('Residual (Observed - Predicted SFR)') plt.title('Residuals vs. Logmass') plt.savefig('residuals_vs_logmass.png') plt.close()
plt.scatter(df[z_col], df[sfr_col] - df['predicted_sfr'], alpha=0.5) plt.xlabel('Redshift (z)') plt.ylabel('Residual (Observed - Predicted SFR)') plt.title('Residuals vs. z') plt.savefig('residuals_vs_z.png') plt.close() print("Saved residual plots ('residuals_vs_logmass.png', 'residuals_vs_z.png').")
# Overall MSE
mse_overall = mean_squared_error(df[sfr_col], df['predicted_sfr']) print(f"\nOverall MSE: {mse_overall:.4f}")
print("\nScript completed!")
