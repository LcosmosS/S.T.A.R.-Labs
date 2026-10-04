# Replace invalid values (-9999) with NaN
df.replace(-9999, np.nan, inplace=True)


# Check for required column
if 'logmass' not in df.columns:
    print("Error: 'logmass' column missing.")
    exit(1)


# Impute missing logmass values with mean
imputer = SimpleImputer(strategy='mean')
df['logmass'] = imputer.fit_transform(df[['logmass']])


# 2. Assign Groups using GMM
gmm = GaussianMixture(n_components=5, random_state=0)
df['groups'] = gmm.fit_predict(df['logmass'].values.reshape(-1, 1))


# Extract Group 2 data (assuming index 1 corresponds to Group 2)
group2_data = df[df['groups'] == 1]
logmass_group2 = group2_data['logmass'].values
mass_group2 = 10 ** logmass_group2  # Convert logmass to mass for power-law fit


# 3. Test Power-Law Distribution
try:
    fit = powerlaw.Fit(mass_group2, verbose=False)
    print(f"\nGroup 2 - Power-law Fit:")
    print(f"Exponent (alpha): {fit.power_law.alpha:.4f}")
    R, p = fit.distribution_compare('power_law', 'lognormal')
    print(f"Power-law vs Lognormal: R = {R:.4f}, p = {p:.4f}")
    if p < 0.05:
        print("Result: Significant difference (power-law preferred if R > 0).")
    else:
        print("Result: No significant difference between distributions.")
except Exception as e:
    print(f"Power-law fit failed: {e}")


# 4. Test Bimodal Distribution
gmm_bimodal = GaussianMixture(n_components=2, random_state=0)
gmm_bimodal.fit(logmass_group2.reshape(-1, 1))
bic_bimodal = gmm_bimodal.bic(logmass_group2.reshape(-1, 1))


gmm_unimodal = GaussianMixture(n_components=1, random_state=0)
gmm_unimodal.fit(logmass_group2.reshape(-1, 1))
bic_unimodal = gmm_unimodal.bic(logmass_group2.reshape(-1, 1))


print(f"\nGroup 2 - Bimodal vs Unimodal Fit:")
print(f"BIC (Bimodal): {bic_bimodal:.4f}")
print(f"BIC (Unimodal): {bic_unimodal:.4f}")
if bic_bimodal < bic_unimodal:
    print("Result: Bimodal distribution is preferred (lower BIC).")
else:
    print("Result: Unimodal distribution is preferred (lower BIC).")


# 5. Visualize Group 2 Logmass Distribution
plt.hist(logmass_group2, bins=30, density=True, color='blue', alpha=0.7)
plt.title("Group 2 Logmass Distribution")
plt.xlabel("logmass")
plt.ylabel("Density")
plt.savefig('group2_logmass_distribution.png')
plt.close()
print("\nSaved Group 2 logmass distribution plot as 'group2_logmass_distribution.png'.")


print("Script completed!")
