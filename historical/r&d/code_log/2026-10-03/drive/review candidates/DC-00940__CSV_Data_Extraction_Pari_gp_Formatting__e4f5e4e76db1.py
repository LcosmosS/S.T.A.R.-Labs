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


# Step 1: Analysis for Group 1, Bin 4 (Group 1 is index 0 in GMM)
group1_indices = (groups == 0)
z_group1 = z[group1_indices]
bins = np.percentile(z_group1, [0, 20, 40, 60, 80, 100])  # 5 bins
bin4_mask = (z_group1 >= bins[4]) & (z_group1 <= bins[5])  # Bin 4 is 80-100%
logmass_bin4 = logmass[group1_indices][bin4_mask]
k_theory_bin4 = compute_K_theory(logmass_bin4)
print(f"Group 1, Bin 4 K_theory: {k_theory_bin4:.4f}")


# Plot RA vs Dec for Bin 4
ra_bin4 = ra[group1_indices][bin4_mask]
dec_bin4 = dec[group1_indices][bin4_mask]
plt.scatter(ra_bin4, dec_bin4)
plt.xlabel("RA")
plt.ylabel("Dec")
plt.title("Group 1, Bin 4: RA vs Dec")
plt.savefig('group1_bin4_positions.png')
plt.close()
print("Saved scatter plot as 'group1_bin4_positions.png'.")


# Step 2: Investigate Group 2 (Group 2 is index 1 in GMM)
group2_indices = (groups == 1)
logmass_group2 = logmass[group2_indices]
plt.hist(logmass_group2, bins=30, density=True)
plt.title("Group 2 Stellar Mass Distribution")
plt.xlabel("logmass")
plt.ylabel("Density")
plt.savefig('group2_logmass_distribution.png')
plt.close()
print("Saved Group 2 logmass distribution as 'group2_logmass_distribution.png'.")


# Step 3: Analyze all groups with median logmass
print("\nAnalysis of all groups:")
for group in range(5):
    group_indices = (groups == group)
    logmass_group = logmass[group_indices]
    k_theory = compute_K_theory(logmass_group)
    median_logmass = np.median(logmass_group)
    print(f"Group {group}: K_theory = {k_theory:.4f}, "
          f"Median z = {np.median(z[group_indices]):.4f}, "
          f"Median SFR = {np.nanmedian(sfr[group_indices]):.4f}, "
          f"Median logmass = {median_logmass:.4f}")


# Step 4: Bin all galaxies by redshift and compute K_theory
print("\nK_theory across redshift bins:")
z_bins = np.percentile(z, [0, 20, 40, 60, 80, 100])  # 5 bins across all data
for i in range(len(z_bins) - 1):
    bin_mask = (z >= z_bins[i]) & (z < z_bins[i + 1])
    logmass_bin = logmass[bin_mask]
    if len(logmass_bin) > 0:  # Ensure bin has data
        k_theory_bin = compute_K_theory(logmass_bin)
        print(f"Redshift bin {i} ({z_bins[i]:.4f} - {z_bins[i+1]:.4f}): K_theory = {k_theory_bin:.4f}")
    else:
        print(f"Redshift bin {i} ({z_bins[i]:.4f} - {z_bins[i+1]:.4f}): No data")


print("\nScript completed successfully!")
