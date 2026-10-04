group1_indices = (groups == 0)
z_group1 = z[group1_indices]
logmass_group1 = logmass[group1_indices]
bins = np.percentile(z_group1, [0, 20, 40, 60, 80, 100])
for i in range(5):
bin_mask = (z_group1 >= bins[i]) & (z_group1 < bins[i+1])


logmass_bin = logmass_group1[bin_mask]


if len(logmass_bin) > 0:


    k_theory_bin = compute_K_theory(logmass_bin)


    print(f"Group 1, Bin {i}: K_theory = {k_theory_bin:.4f}, Median z = {np.median(z_group1[bin_mask]):.4f}")
