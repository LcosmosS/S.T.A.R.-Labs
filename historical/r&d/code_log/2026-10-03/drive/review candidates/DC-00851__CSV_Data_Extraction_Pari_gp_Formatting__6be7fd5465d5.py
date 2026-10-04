# Extract z, sfr, and ra for group averaging
z = valid_df['z'].values
sfr = valid_df['sfr'].values
ra = valid_df['ra'].values


# Compute and print averages for each group
for i in range(gmm.n_components):
    group_logmass = logmass[groups == i]
    group_z = z[groups == i]
    group_sfr = sfr[groups == i]
    group_ra = ra[groups == i]
    print(f"Group {i}:")
    print(f"  Avg z = {np.mean(group_z)}")
    print(f"  Avg sfr = {np.mean(group_sfr)}")
    print(f"  Avg ra = {np.mean(group_ra)}")
    print(f"  Number of galaxies = {len(group_logmass)}")
