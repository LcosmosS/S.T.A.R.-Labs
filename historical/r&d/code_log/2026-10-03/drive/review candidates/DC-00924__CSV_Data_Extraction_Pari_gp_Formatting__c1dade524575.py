if missing_columns:
    print(f"Error: Missing columns in the CSV file: {missing_columns}")
    exit(1)


# Step 3: Remove rows with NaN in 'logmass' for GMM fitting
df_clean = df.dropna(subset=['logmass'])


# Extract cleaned data
z = df_clean['z'].values
sfr = df_clean['sfr'].values
ra = df_clean['ra'].values
dec = df_clean['dec'].values
logmass = df_clean['logmass'].values


# Step 4: Fit Gaussian Mixture Model (GMM) with 5 components to logmass
try:
    gmm = GaussianMixture(n_components=5, random_state=0).fit(logmass.reshape(-1, 1))
    groups = gmm.predict(logmass.reshape(-1, 1))
    print(f"Fitted GMM with 5 components to 'logmass' data.")
except ValueError as e:
    print(f"Error: GMM fitting failed. Check 'logmass' data: {e}")
    exit(1)


# Step 5: Define the correct K_theory calculation function
def compute_K_theory(logmass_vec):
    """Compute K_theory based on BSD Cosmology theory."""
    M = 10 ** logmass_vec  # Convert logmass to stellar mass
    M0 = np.median(M)      # Median mass
    sum_M_over_M0 = np.sum(M / M0)
    sum_M0_over_M = np.sum(M0 / M)
    return sum_M_over_M0 / sum_M0_over_M


# Step 6: Analysis for Group 1, Bin 4
# Note: GMM labels groups as 0-4; Group 1 is index 0
group1_indices = (groups == 0)
z_group1 = z[group1_indices]


# Define 5 bins based on redshift percentiles (0-20%, 20-40%, 40-60%, 60-80%, 80-100%)
bins = np.percentile(z_group1, [0, 20, 40, 60, 80, 100])
bin4_mask = (z_group1 >= bins[4]) & (z_group1 <= bins[5])  # Bin 4 is 80-100%
z_bin4 = z_group1[bin4_mask]
print(f"Bin 4 redshift range: {np.min(z_bin4):.4f} to {np.max(z_bin4):.4f}")


# Calculate average SFR for Bin 4, ignoring NaN values
sfr_bin4 = sfr[group1_indices][bin4_mask]
avg_sfr = np.nanmean(sfr_bin4)
print(f"Bin 4 average SFR: {avg_sfr:.4f}")


# RA and Dec ranges for Bin 4
ra_bin4 = ra[group1_indices][bin4_mask]
dec_bin4 = dec[group1_indices][bin4_mask]
print(f"Bin 4 RA range: {np.min(ra_bin4):.4f} to {np.max(ra_bin4):.4f}")
print(f"Bin 4 Dec range: {np.min(dec_bin4):.4f} to {np.max(dec_bin4):.4f}")


# Plot RA vs Dec for Bin 4 and save the figure
plt.scatter(ra_bin4, dec_bin4)
plt.xlabel("RA")
plt.ylabel("Dec")
plt.title("Group 1, Bin 4: RA vs Dec")
plt.savefig('group1_bin4_positions.png')
plt.close()
print("Saved scatter plot as 'group1_bin4_positions.png'.")


# Step 7: Analysis for Group 2
# Note: Group 2 is index 1 in GMM output
group2_indices = (groups == 1)
logmass_group2 = logmass[group2_indices]


# Bootstrap K_theory calculation for Group 2 (1000 resamples)
k_theory_values = []
for _ in range(1000):
    resample = np.random.choice(logmass_group2, size=len(logmass_group2), replace=True)
    k_theory = compute_K_theory(resample)
    k_theory_values.append(k_theory)


mean_k = np.mean(k_theory_values)
std_k = np.std(k_theory_values)
print(f"Group 2 K_theory: mean = {mean_k:.4f}, std = {std_k:.4f}")


# Calculate averages for Group 2, ignoring NaN values
z_group2 = z[group2_indices]
sfr_group2 = sfr[group2_indices]
ra_group2 = ra[group2_indices]
print(f"Group 2 averages: z = {np.mean(z_group2):.4f}, SFR = {np.nanmean(sfr_group2):.4f}, RA = {np.mean(ra_group2):.4f}")
