# After filtering (valid_df is defined)
logmass = valid_df['logmass'].values  # Extract logmass as NumPy array
gmm = GaussianMixture(n_components=3).fit(logmass.reshape(-1, 1))
groups = gmm.predict(logmass.reshape(-1, 1))


# Define arrays for group averages
z = valid_df['z'].values
sfr = valid_df['sfr'].values
ra = valid_df['ra'].values


for i in range(3):
    group_logmass = logmass[groups == i]
    group_z = z[groups == i]  # No need for np.array() since z is already a NumPy array
    group_sfr = sfr[groups == i]
    group_ra = ra[groups == i]
    print(f"Group {i}: Avg z = {np.mean(group_z)}, Avg sfr = {np.mean(group_sfr)}, Avg ra = {np.mean(group_ra)}")
