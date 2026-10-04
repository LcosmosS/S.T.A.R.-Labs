# Step 7: Extract 'z', 'sfr', and 'ra' for group averaging
z = valid_df['z'].values sfr = valid_df['sfr'].values ra = valid_df['ra'].values
# Step 8: Compute and print averages for each GMM group
for i in range(gmm.n_components): group_logmass = logmass[groups == i] group_z = z[groups == i] group_sfr = sfr[groups == i] group_ra = ra[groups == i] print(f"\nGroup {i}:") print(f" Average z = {np.mean(group_z):.4f}") print(f" Average sfr = {np.mean(group_sfr):.4f}") print(f" Average ra = {np.mean(group_ra):.4f}") print(f" Number of galaxies = {len(group_logmass)}")
print("\nScript completed successfully!")
