# Impute missing values with mean
imputer = SimpleImputer(strategy='mean') df[['logmass', 'z']] = imputer.fit_transform(df[['logmass', 'z']])
# 2. Assign Groups using GMM (5 components)
gmm = GaussianMixture(n_components=5, random_state=0) df['groups'] = gmm.fit_predict(df['logmass'].values.reshape(-1, 1))
# Extract Group 2 data (index 1)
group2_data = df[df['groups'] == 1] logmass_group2 = group2_data['logmass'].values
# 3. Fit Bimodal GMM to Group 2
gmm_bimodal = GaussianMixture(n_components=2, random_state=0) gmm_bimodal.fit(logmass_group2.reshape(-1, 1)) subgroups = gmm_bimodal.predict(logmass_group2.reshape(-1, 1)) group2_data['subgroup'] = subgroups # Add subgroup labels (0 or 1)
# 4. Analyze Physical Properties of Subgroups
subgroup0 = group2_data[group2_data['subgroup'] == 0] subgroup1 = group2_data[group2_data['subgroup'] == 1]
# Redshift (z) analysis
print("\nSubgroup 0 - Redshift Analysis:") print(f"Mean z: {subgroup0['z'].mean():.4f}, Median z: {subgroup0['z'].median():.4f}") print("\nSubgroup 1 - Redshift Analysis:") print(f"Mean z: {subgroup1['z'].mean():.4f}, Median z: {subgroup1['z'].median():.4f}")
# Morphology analysis (assuming 'morphology' is categorical)
print("\nSubgroup 0 - Morphology Distribution:") print(subgroup0['morphology'].value_counts(normalize=True)) print("\nSubgroup 1 - Morphology Distribution:") print(subgroup1['morphology'].value_counts(normalize=True))
# 5. Revisit Power-Law Test with Adjusted Mass Range # Option 1: Remove extreme values (e.g., top 1% and bottom 1%)
mass_group2 = 10 ** logmass_group2 mass_filtered = mass_group2[(mass_group2 > np.percentile(mass_group2, 1)) & (mass_group2 < np.percentile(mass_group2, 99))]
# Option 2: Use logmass directly (if mass causes overflow) # mass_filtered = logmass_group2 # Uncomment to test on logmass # Fit power-law to filtered data
try: fit = powerlaw.Fit(mass_filtered, verbose=False) print(f"\nAdjusted Power-law Fit (Filtered Data):") print(f"Exponent (alpha): {fit.power_law.alpha:.4f}") R, p = fit.distribution_compare('power_law', 'lognormal') print(f"Power-law vs Lognormal: R = {R:.4f}, p = {p:.4f}") if p < 0.05 and R > 0: print("Result: Power-law is preferred over lognormal.") else: print("Result: No significant preference for power-law.") except Exception as e: print(f"Adjusted power-law fit failed: {e}")
# 6. Visualize Subgroups
plt.hist(subgroup0['logmass'], bins=15, alpha=0.5, label='Subgroup 0', density=True) plt.hist(subgroup1['logmass'], bins=15, alpha=0.5, label='Subgroup 1', density=True) plt.title("Group 2 Subpopulations Logmass Distribution") plt.xlabel("logmass") plt.ylabel("Density") plt.legend() plt.savefig('group2_subpopulations_logmass.png') plt.close() print("\nSaved Group 2 subpopulations plot as 'group2_subpopulations_logmass.png'.")
print("Script completed!")
