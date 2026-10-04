# Extract 'logmass' for GMM (assuming 'logmass' is a column in your CSV)
logmass = df['logmass'].values.reshape(-1, 1)
# Determine optimal number of GMM components using BIC
n_components_range = range(1, 11) bic_scores = [] for n in n_components_range: gmm = GaussianMixture(n_components=n, random_state=42) gmm.fit(logmass) bic_scores.append(gmm.bic(logmass))
# Select the optimal number of components
optimal_n = n_components_range[np.argmin(bic_scores)] print(f"Optimal number of components: {optimal_n}")
# Fit the GMM with the optimal number of components
best_gmm = GaussianMixture(n_components=optimal_n, random_state=42) best_gmm.fit(logmass) df['subpopulation'] = best_gmm.predict(logmass)
# Compute 'mass' from 'logmass' (assuming mass is in solar units)
df['mass'] = 10 ** df['logmass']
# Compute K_values for each subpopulation
grouped = df.groupby('subpopulation') K_values = {} for subpop, group in grouped: masses = group['mass'].values M0 = np.median(masses) sum_M_over_M0 = np.sum(masses / M0) sum_M0_over_M = np.sum(M0 / masses) K = sum_M_over_M0 / sum_M0_over_M K_values[subpop] = K print(f"Subpopulation {subpop}: M0 = {M0:.2e}, K = {K:.4f}")
# Compute rank
