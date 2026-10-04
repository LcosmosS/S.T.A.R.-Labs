if missing_columns:
    print(f"Error: Missing columns in the CSV file: {missing_columns}")
    exit(1)


# Remove rows with NaN in 'logmass' for GMM fitting
df_clean = df.dropna(subset=['logmass'])


# Extract cleaned data
z = df_clean['z'].values
sfr = df_clean['sfr'].values
ra = df_clean['ra'].values
dec = df_clean['dec'].values
logmass = df_clean['logmass'].values


# Fit Gaussian Mixture Model (GMM) with 5 components to logmass
try:
    gmm = GaussianMixture(n_components=5, random_state=0).fit(logmass.reshape(-1, 1))
    groups = gmm.predict(logmass.reshape(-1, 1))
    print(f"Fitted GMM with 5 components to 'logmass' data.")
except ValueError as e:
    print(f"Error: GMM fitting failed. Check 'logmass' data: {e}")
    exit(1)


# Define the K_theory calculation function
def compute_K_theory(logmass_vec):
    """Compute K_theory based on BSD Cosmology theory."""
    M = 10 ** logmass_vec  # Convert logmass to stellar mass
    M0 = np.median(M)      # Median mass
    sum_M_over_M0 = np.sum(M / M0)
    sum_M0_over_M = np.sum(M0 / M)
    return sum_M_over_M0 / sum_M0_over_M


# Analysis for Group 1, Bin 4 (Group 1 is index 0 in GMM)
group1_indices = (groups == 0)
z_group1 = z[group1_indices]


# Define 5 bins based on redshift percentiles (0-20%, 20-40%, 40-60%, 60-80%, 80-100%)
bins = np.percentile(z_group1, [0, 20, 40, 60, 80, 100])
bin4_mask = (z_group1 >= bins[4]) & (z_group1 <= bins[5])  # Bin 4 is 80-100%
logmass_bin4 = logmass[group1_indices][bin4_mask]


# Calculate K_theory for Group 1, Bin 4
k_theory_bin4 = compute_K_theory(logmass_bin4)
print(f"Group 1, Bin 4 K_theory: {k_theory_bin4:.4f}")


# Analysis for Group 2 (Group 2 is index 1 in GMM)
group2_indices = (groups == 1)
logmass_group2 = logmass[group2_indices]


# Plot stellar mass distribution for Group 2
plt.hist(logmass_group2, bins=30, density=True)
plt.title("Group 2 Stellar Mass Distribution")
plt.xlabel("logmass")
plt.ylabel("Density")
plt.savefig('group2_logmass_distribution.png')
plt.close()
print("Saved Group 2 logmass distribution as 'group2_logmass_distribution.png'.")


# Calculate and print median properties for Group 2
print(f"Group 2 - Median z: {np.median(z[group2_indices]):.4f}")
print(f"Group 2 - Median SFR: {np.median(sfr[group2_indices]):.4f}")


# Visualize Group 1, Bin 4 positions
ra_bin4 = ra[group1_indices][bin4_mask]
dec_bin4 = dec[group1_indices][bin4_mask]
plt.scatter(ra_bin4, dec_bin4)
plt.xlabel("RA")
plt.ylabel("Dec")
plt.title("Group 1, Bin 4: RA vs Dec")
plt.savefig('group1_bin4_positions.png')
plt.close()
print("Saved scatter plot as 'group1_bin4_positions.png'.")


# Expand analysis to other groups
for group in range(5):
    group_indices = (groups == group)
    logmass_group = logmass[group_indices]
    k_theory = compute_K_theory(logmass_group)
    print(f"Group {group}: K_theory = {k_theory:.4f}, "
          f"Median z = {np.median(z[group_indices]):.4f}, "
          f"Median SFR = {np.median(sfr[group_indices]):.4f}")
