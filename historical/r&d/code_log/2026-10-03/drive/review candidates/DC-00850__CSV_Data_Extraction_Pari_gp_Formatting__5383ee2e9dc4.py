except Exception as e:
    print(f"Error: An unexpected error occurred while writing to '{pari_gp_file}': {e}")
    exit(1)


# Extract logmass for GMM fitting
logmass = valid_df['logmass'].values


# Fit GMM with 3 components (you can adjust n_components based on your needs)
try:
    gmm = GaussianMixture(n_components=3, random_state=0).fit(logmass.reshape(-1, 1))
    groups = gmm.predict(logmass.reshape(-1, 1))
except ValueError as e:
