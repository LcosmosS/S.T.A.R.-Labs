# Replace invalid data (-9999) with NaN
df.replace(-9999, np.nan, inplace=True)


# Verify required columns
required_columns = ['z', 'sfr', 'ra', 'dec', 'logmass']
if not all(col in df.columns for col in required_columns):
    print("Error: Missing required columns.")
    exit(1)


# Impute missing logmass values
imputer = SimpleImputer(strategy='mean')
df['logmass'] = imputer.fit_transform(df[['logmass']])


# Fit GMM to assign groups
gmm = GaussianMixture(n_components=5, random_state=0)
df['groups'] = gmm.fit_predict(df['logmass'].values.reshape(-1, 1))


# Define K_theory calculation
def compute_K_theory(logmass):
    M = 10 ** logmass
    M0 = np.median(M)
    return np.sum(M / M0) / np.sum(M0 / M)


# Step 1: Test Alternative Distributions for Group 2
group2_data = df[df['groups'] == 1]  # Group 2 is index 1
logmass_group2 = group2_data['logmass'].values
mass_group2 = 10 ** logmass_group2


# Test power-law distribution
try:
    fit = powerlaw.Fit(mass_group2, verbose=False)
    print(f"Group 2 - Power-law fit: exponent = {fit.power_law.alpha:.4f}")
    R, p = fit.distribution_compare('power_law', 'lognormal')
    print(f"Group 2 - Power-law vs lognormal: R = {R:.4f}, p = {p:.4f}")
except Exception as e:
    print(f"Power-law fit failed: {e}")


# Test bimodal distribution
gmm_bimodal = GMM_bimodal(n_components=2, random_state=0)
gmm_bimodal.fit(logmass_group2.reshape(-1, 1))
bic_bimodal = gmm_bimodal.bic(logmass_group2.reshape(-1, 1))
gmm_unimodal = GMM_bimodal(n_components=1, random_state=0)
gmm_unimodal.fit(logmass_group2.reshape(-1, 1))
bic_unimodal = gmm_unimodal.bic(logmass_group2.reshape(-1, 1))
print(f"Group 2 - Bimodal vs Unimodal: BIC (bimodal) = {bic_bimodal:.4f}, BIC (unimodal) = {bic_unimodal:.4f}")


# Step 2: Investigate Group 4 Properties
group4_data = df[df['groups'] == 4]  # Group 4 is index 4
print("\nGroup 4 Properties:")
print(f"Median logmass: {np.median(group4_data['logmass']):.4f}")
print(f"Median SFR: {np.nanmedian(group4_data['sfr']):.4f}")
print(f"Median redshift: {np.median(group4_data['z']):.4f}")


# Step 3: Group-Specific Tweaks for K_theory
def adjusted_K_theory(logmass, sfr, alpha, beta):
    k_theory = compute_K_theory(logmass)
    return k_theory * (1 + alpha) * (1 + beta * sfr)


# Apply group-specific adjustments
for group in range(5):
    group_data = df[df['groups'] == group]
    logmass = group_data['logmass'].values
    sfr = np.nanmedian(group_data['sfr'])
    k_theory = compute_K_theory(logmass)
    
    # Group-specific α and β (example values, adjust based on optimization)
    alpha = 0.1 if group in [0, 2, 3] else 0.05  # Higher for better-fitting groups
    beta = -0.1 if group == 4 else 0.05  # Negative for low-SFR Group 4
    k_adjusted = adjusted_K_theory(logmass, sfr, alpha, beta)
    print(f"Group {group}: K_theory = {k_theory:.4f}, Adjusted K_theory = {k_adjusted:.4f}")


# Plot Group 2’s mass distribution
plt.hist(logmass_group2, bins=30, density=True)
plt.title("Group 2 Logmass Distribution")
plt.xlabel("logmass")
plt.ylabel("Density")
plt.savefig('group2_logmass_distribution.png')
plt.close()
print("Saved Group 2 distribution plot.")


print("Script completed!")
