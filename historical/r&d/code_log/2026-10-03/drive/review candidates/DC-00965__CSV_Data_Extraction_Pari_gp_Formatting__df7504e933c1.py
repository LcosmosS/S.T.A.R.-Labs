if missing_columns:
    print(f"Error: Missing columns in the CSV file: {missing_columns}")
    exit(1)


# Handle missing values in logmass with mean imputation
imputer = SimpleImputer(strategy='mean')
df['logmass'] = imputer.fit_transform(df[['logmass']])


# Fit Gaussian Mixture Model (GMM) with 5 components to logmass
try:
    gmm = GaussianMixture(n_components=5, random_state=0).fit(df['logmass'].values.reshape(-1, 1))
    df['groups'] = gmm.predict(df['logmass'].values.reshape(-1, 1))
    print(f"Fitted GMM with 5 components to 'logmass' data.")
except ValueError as e:
    print(f"Error: GMM fitting failed. Check 'logmass' data: {e}")
    exit(1)


# Define K_theory calculation function
def compute_K_theory(logmass_vec):
    M = 10 ** logmass_vec
    M0 = np.median(M)
    sum_M_over_M0 = np.sum(M / M0)
    sum_M0_over_M = np.sum(M0 / M)
    return sum_M_over_M0 / sum_M0_over_M


# Step 1: Refine Mass Distribution for Group 2
group2_indices = (df['groups'] == 1)  # Group 2 is index 1
logmass_group2 = df[group2_indices]['logmass'].values
mass_group2 = 10 ** logmass_group2


# Test power-law distribution
fit = powerlaw.Fit(mass_group2, verbose=False)
print(f"Power-law fit for Group 2: exponent = {fit.power_law.alpha:.4f}")
R, p = fit.distribution_compare('power_law', 'lognormal')
print(f"Power-law vs lognormal: log-likelihood ratio = {R:.4f}, p-value = {p:.4f}")


# Step 2: Incorporate Environmental Density
def calculate_local_density(ra, dec, radius=1.0):
    density = []
    for i in range(len(ra)):
        dist = np.sqrt((ra - ra[i])**2 + (dec - dec[i])**2)
        density.append(np.sum(dist < radius))
    return np.array(density)


df['local_density'] = calculate_local_density(df['ra'].values, df['dec'].values)
df['scaled_density'] = (df['local_density'] - df['local_density'].min()) / (df['local_density'].max() - df['local_density'].min())


# Step 3: Account for SFR
median_sfr = df.groupby('groups')['sfr'].median()


# Step 4: Adjust K_theory
alpha = 0.1  # Density correction factor
beta = 0.05  # SFR correction factor


for group in range(5):
    group_data = df[df['groups'] == group]
    logmass_group = group_data['logmass'].values
    k_theory = compute_K_theory(logmass_group)
    scaled_density = group_data['scaled_density'].mean()
    median_sfr_group = median_sfr[group]
    k_theory_adjusted = k_theory * (1 + alpha * scaled_density) * (1 + beta * median_sfr_group)
    print(f"Group {group}: Original K_theory = {k_theory:.4f}, Adjusted K_theory = {k_theory_adjusted:.4f}")


# Step 5: Validate Adjustments
original_mse = np.mean([(compute_K_theory(df[df['groups'] == group]['logmass'].values) - 1)**2 for group in range(5)])
adjusted_mse = np.mean([(compute_K_theory(df[df['groups'] == group]['logmass'].values) * 
                        (1 + alpha * df[df['groups'] == group]['scaled_density'].mean()) * 
                        (1 + beta * median_sfr[group]) - 1)**2 for group in range(5)])
print(f"Original MSE: Ascending: {original_mse:.4f}, Adjusted MSE: {adjusted_mse:.4f}")


# Plot mass distribution for Group 2
plt.hist(logmass_group2, bins=30, density=True)
plt.title("Group 2 Stellar Mass Distribution")
plt.xlabel("logmass")
plt.ylabel("Density")
plt.savefig('group2_logmass_distribution.png')
plt.close()
print("Saved Group 2 logmass distribution as 'group2_logmass_distribution.png'.")


print("\nScript completed successfully!")
