# Perform GMM clustering
gmm = GaussianMixture(n_components=5, random_state=0)
groups = gmm.fit_predict(logmass.reshape(-1, 1))
print("Fitted GMM with 5 components to 'logmass' data.")


# Correct K_theory calculation
def compute_K_theory(logmass_vec):
    M = 10 ** logmass_vec  # Convert logmass to mass
    M_sorted = np.sort(M)
    n = len(M)
    if n == 0:
        return 0
    # Median mass
    if n % 2 == 1:
        M0 = M_sorted[n // 2]
    else:
        M0 = (M_sorted[n // 2 - 1] + M_sorted[n // 2]) / 2
    sum_M_over_M0 = np.sum(M / M0)
    sum_M0_over_M = np.sum(M0 / M)
    return sum_M_over_M0 / sum_M0_over_M


# Group 1's Bin 4 analysis
group1_indices = (groups == 1)
z_group1 = z[group1_indices]
bins = np.percentile(z_group1, [0, 20, 40, 60, 80, 100])  # 5 bins
bin4_mask = (z_group1 >= bins[4]) & (z_group1 <= bins[5])  # Bin 4 (80-100 percentile)
z_bin4 = z_group1[bin4_mask]
print(f"Bin 4 redshift range: {np.min(z_bin4):.4f} to {np.max(z_bin4):.4f}")


# Exclude NaN sfr values when calculating average
sfr_bin4 = sfr[group1_indices][bin4_mask]
sfr_bin4_valid = sfr_bin4[~np.isnan(sfr_bin4)]
if len(sfr_bin4_valid) > 0:
    avg_sfr = np.mean(sfr_bin4_valid)
    print(f"Bin 4 average sfr: {avg_sfr:.4f}")
else:
    print("Bin 4: No valid sfr data available.")


ra_bin4 = ra[group1_indices][bin4_mask]
dec_bin4 = dec[group1_indices][bin4_mask]
print(f"Bin 4 ra range: {np.min(ra_bin4):.4f} to {np.max(ra_bin4):.4f}")
print(f"Bin 4 dec range: {np.min(dec_bin4):.4f} to {np.max(dec_bin4):.4f}")


plt.scatter(ra_bin4, dec_bin4)
plt.xlabel("RA")
plt.ylabel("Dec")
plt.savefig('group1_bin4_positions.png')


# Group 2 analysis
group2_indices = (groups == 2)
logmass_group2 = logmass[group2_indices]
k_theory_values = []


for _ in range(1000):
    resample = np.random.choice(logmass_group2, size=len(logmass_group2), replace=True)
    k_theory = compute_K_theory(resample)
    k_theory_values.append(k_theory)


mean_k = np.mean(k_theory_values)
std_k = np.std(k_theory_values)
print(f"Group 2 K_theory: mean = {mean_k:.4f}, std = {std_k:.4f}")


# Exclude NaN sfr values for Group 2
z_group2 = z[group2_indices]
sfr_group2 = sfr[group2_indices]
ra_group2 = ra[group2_indices]
valid_sfr_mask = ~np.isnan(sfr_group2)
if np.sum(valid_sfr_mask) > 0:
    avg_sfr_group2 = np.mean(sfr_group2[valid_sfr_mask])
else:
    avg_sfr_group2 = np.nan
print(f"Group 2: z = {np.mean(z_group2):.4f}, sfr = {avg_sfr_group2 if not np.isnan(avg_sfr_group2) else 'No valid data'}, ra = {np.mean(ra_group2):.4f}")
