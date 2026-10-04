except Exception as e:
    print(f"Error: Failed to write to '{pari_gp_file}': {e}")
    exit(1)


# Step 5: Extract 'logmass' for GMM fitting
logmass = valid_df['logmass'].values


# Step 6: Fit a Gaussian Mixture Model (GMM) with 3 components
try:
    gmm = GaussianMixture(n_components=3, random_state=0).fit(logmass.reshape(-1, 1))
    groups = gmm.predict(logmass.reshape(-1, 1))
    print(f"Fitted GMM with 3 components to 'logmass' data.")
except ValueError as e:
    print(f"Error: GMM fitting failed. Check 'logmass' data: {e}")
    exit(1)


# Step 7: Extract 'z', 'sfr', and 'ra' for group averaging
z = valid_df['z'].values
sfr = valid_df['sfr'].values
ra = valid_df['ra'].values


# Step 8: Compute and print averages for each GMM group
for i in range(gmm.n_components):
    group_logmass = logmass[groups == i]
    group_z = z[groups == i]
    group_sfr = sfr[groups == i]
    group_ra = ra[groups == i]
    print(f"\nGroup {i}:")
    print(f"  Average z = {np.mean(group_z):.4f}")
    print(f"  Average sfr = {np.mean(group_sfr):.4f}")
    print(f"  Average ra = {np.mean(group_ra):.4f}")
    print(f"  Number of galaxies = {len(group_logmass)}")


print("\nScript completed successfully!")
