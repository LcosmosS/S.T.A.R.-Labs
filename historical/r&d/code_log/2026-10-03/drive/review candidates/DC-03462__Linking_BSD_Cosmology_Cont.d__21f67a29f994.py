# Handle missing values
imputer = SimpleImputer(strategy='mean') df[[logmass_col, z_col, sfr_col]] = imputer.fit_transform(df[[logmass_col, z_col, sfr_col]])
# **Incorporate Quenching Mechanisms**
def bsd_predicted_sfr(logmass, z, quenching=True, mass_threshold=10.5, gamma=0.2): """ BSD SFR prediction with optional quenching. Base: SFR = 0.5 * logmass - 0.1 * z (placeholder; replace with actual BSD formula). Quenching: Reduces SFR for high-mass galaxies (logmass > threshold). """ base_sfr = 0.5 * logmass - 0.1 * z # Placeholder BSD formula if quenching: quenching_term = -gamma * np.maximum(logmass - mass_threshold, 0) return base_sfr + quenching_term return base_sfr
# Compute predicted SFR with quenching
df['predicted_sfr'] = bsd_predicted_sfr(df[logmass_col], df[z_col])
# **Group-Specific Adjustments** # Bin logmass into quartiles if 'group' not present
if 'group' not in df.columns: df['group'] = pd.cut(df[logmass_col], bins=4, labels=['Low', 'Mid-Low', 'Mid-High', 'High']) print("Created 'group' column by binning logmass into 4 quartiles.")
# Compute MSE per group
mse_per_group = df.groupby('group').apply( lambda x: mean_squared_error(x[sfr_col], x['predicted_sfr']) ) print("\nMSE per Group:") print(mse_per_group)
# Plot observed vs. predicted SFR per group
for group in df['group'].unique(): group_data = df[df['group'] == group] plt.scatter(group_data[sfr_col], group_data['predicted_sfr'], alpha=0.5) plt.xlabel('Observed SFR') plt.ylabel('Predicted SFR') plt.title(f'Observed vs. Predicted SFR - {group}') plt.plot([group_data[sfr_col].min(), group_data[sfr_col].max()], [group_data[sfr_col].min(), group_data[sfr_col].max()], 'r--') plt.savefig(f'observed_vs_predicted_sfr_{group}.png') plt.close() print("Saved group-specific SFR plots (e.g., 'observed_vs_predicted_sfr_Low.png').")
# **Enhance Mass and Redshift Terms** # Add polynomial features (logmass^2, z^2, logmass*z)
poly = PolynomialFeatures(degree=2, include_bias=False) X_poly = poly.fit_transform(df[[logmass_col, z_col]]) poly_model = LinearRegression().fit(X_poly, df[sfr_col]) df['predicted_sfr_poly'] = poly_model.predict(X_poly) mse_poly = mean_squared_error(df[sfr_col], df['predicted_sfr_poly']) print(f"\nMSE with Polynomial Terms: {mse_poly:.4f}")
# Coefficients for interpretation
feature_names = poly.get_feature_names_out([logmass_col, z_col]) print("Polynomial Model Coefficients:") for name, coef in zip(feature_names, poly_model.coef_): print(f"{name}: {coef:.4f}")
# **Explore Advanced Techniques (Machine Learning)** # Random Forest example (uncomment to use)
""" rf_model = RandomForestRegressor(n_estimators=100, random_state=42) rf_model.fit(df[[logmass_col, z_col]], df[sfr_col]) df['predicted_sfr_rf'] = rf_model.predict(df[[logmass_col, z_col]]) mse_rf = mean_squared_error(df[sfr_col], df['predicted_sfr_rf']) print(f"MSE with Random Forest: {mse_rf:.4f}") """
# Overall MSE with quenching
mse_base = mean_squared_error(df[sfr_col], df['predicted_sfr']) print(f"\nOverall MSE with Quenching: {mse_base:.4f}")
# Residual plots
plt.scatter(df[logmass_col], df[sfr_col] - df['predicted_sfr'], alpha=0.5) plt.xlabel('Logmass') plt.ylabel('Residual (Observed - Predicted SFR)') plt.title('Residuals vs. Logmass') plt.savefig('residuals_vs_logmass.png') plt.close()
plt.scatter(df[z_col], df[sfr_col] - df['predicted_sfr'], alpha=0.5) plt.xlabel('Redshift (z)') plt.ylabel('Residual (Observed - Predicted SFR)') plt.title('Residuals vs. z') plt.savefig('residuals_vs_z.png') plt.close() print("Saved residual plots ('residuals_vs_logmass.png', 'residuals_vs_z.png').")
print("\nScript completed successfully!")
