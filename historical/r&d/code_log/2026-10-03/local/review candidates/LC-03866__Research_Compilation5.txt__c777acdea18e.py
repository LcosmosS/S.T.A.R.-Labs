# Filter out rows with -9999 in columns_to_filter
df = df[(df[columns_to_filter] != -9999).all(axis=1)]
print(f"Number of valid rows after filtering: {len(df)}")


# Extract logmass for GMM
logmass = df['logmass'].values.reshape(-1, 1)


# Test 1 to 10 components using BIC
n_components_range = range(1, 11)
bic_scores = []
for n in n_components_range:
    gmm = GaussianMixture(n_components=n, random_state=42)
    gmm.fit(logmass)
    bic_scores.append(gmm.bic(logmass))


# Choose the best model
optimal_n = n_components_range[np.argmin(bic_scores)]
print(f"Optimal number of components: {optimal_n}")


# Fit the best model and assign subpopulations
best_gmm = GaussianMixture(n_components=optimal_n, random_state=42)
best_gmm.fit(logmass)
df['subpopulation'] = best_gmm.predict(logmass)


# Compute mass for PARI/GP
df['mass'] = 10 ** df['logmass']


# Compute K_values
grouped = df.groupby('subpopulation')
K_values = {}
for subpop, group in grouped:
    masses = group['mass'].values
    M0 = np.median(masses)
    sum_M_over_M0 = np.sum(masses / M0)
    sum_M0_over_M = np.sum(M0 / masses)
    K = sum_M_over_M0 / sum_M0_over_M
    K_values[subpop] = K
    print(f"Subpopulation {subpop}: M0 = {M0:.2e}, K = {K:.4f}")


# Compute rank
