# Perform GMM clustering to assign groups based on logmass
try:
    gmm = GaussianMixture(n_components=5, random_state=0)  # 5 groups, adjust as needed
    groups = gmm.fit_predict(logmass.reshape(-1, 1))
    print("Fitted GMM with 5 components to 'logmass' data.")
except ValueError as e:
    print(f"Error: GMM fitting failed. Check 'logmass' data: {e}")
    exit(1)


# Define compute_K_theory function
def compute_K_theory(logmass_vec):
    return np.mean(logmass_vec)  # Replace with actual calculation if needed


# Group 1's Bin 4 analysis
group1_indices = (groups == 1)  # Note: Groups are 0-indexed (0 to 4), adjust if needed
z_group1 = z[group1_indices]
bins = np.percentile(z_group1, [0, 20, 40, 60, 80, 100])  # 5 bins
bin4_mask = (z_group1 >= bins[3]) & (z_group1 <= bins[4])  # Bin 4 (80-100 percentile)
z_bin4 = z_group1[bin4_mask]
print(f"Bin 4 redshift range: {np.min(z_bin4):.4f} to {np.max(z_bin4):.4f}")


sfr_bin4 = sfr[group1_indices][bin4_mask]
avg_sfr = np.mean(sfr_bin4)
print(f"Bin 4 average sfr: {avg_sfr:.4f}")


ra_bin4 = ra[group1_indices][bin4_mask]
dec_bin4 = dec[group1_indices][bin4_mask]
print(f"Bin 4 ra range: {np.min(ra_bin4):.4f} to {np.max(ra_bin4):.4f}")
print(f"Bin 4 dec range: {np.min(dec_bin4):.4f} to {np.max(dec_bin4):.4f}")


plt.scatter(ra_bin4, dec_bin4)
plt.xlabel("RA")
plt.ylabel("Dec")
plt.savefig('group1_bin4_positions.png')
# plt.show()  # Uncomment to display the plot instead of saving


# Group 2 analysis
group2_indices = (groups == 2)  # Adjust group number if needed
logmass_group2 = logmass[group2_indices]
k_theory_values = []


for _ in range(1000):
    resample = np.random.choice(logmass_group2, size=len(logmass_group2), replace=True)
    k_theory = compute_K_theory(resample)
    k_theory_values.append(k_theory)


mean_k = np.mean(k_theory_values)
std_k = np.std(k_theory_values)
print(f"Group 2 K_theory: mean = {mean_k:.4f}, std = {std_k:.4f}")


z_group2 = z[group2_indices]
sfr_group2 = sfr[group2_indices]
ra_group2 = ra[group2_indices]
print(f"Group 2: z = {np.mean(z_group2):.4f}, sfr = {np.mean(sfr_group2):.4f}, ra = {np.mean(ra_group2):.4f}")
