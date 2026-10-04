    print(f"File not found: {file_path}")
    exit(1)


# Extract 'logmass' for GMM (assuming 'logmass' is a column in your CSV)
logmass = df['logmass'].values.reshape(-1, 1)


# Determine optimal number of GMM components using BIC
n_components_range = range(1, 11)
bic_scores = []
for n in n_components_range:
    gmm = GaussianMixture(n_components=n, random_state=42)
    gmm.fit(logmass)
    bic_scores.append(gmm.bic(logmass))


# Select the optimal number of components
optimal_n = n_components_range[np.argmin(bic_scores)]
print(f"Optimal number of components: {optimal_n}")


# Fit the GMM with the optimal number of components
best_gmm = GaussianMixture(n_components=optimal_n, random_state=42)
best_gmm.fit(logmass)
df['subpopulation'] = best_gmm.predict(logmass)


# Compute 'mass' from 'logmass' (assuming mass is in solar units)
df['mass'] = 10 ** df['logmass']


# Compute K_values for each subpopulation
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
rank = sum(1 for K in K_values.values() if abs(K - 1) < 0.1)
print(f"Rank: {rank}")


# Print subpopulation counts
print(df['subpopulation'].value_counts())


# Plot histograms for 'logmass'
plt.figure(figsize=(10, 6))
for i in range(optimal_n):
    subset = df[df['subpopulation'] == i]
    plt.hist(subset['logmass'], bins=50, alpha=0.5, label=f'Subpop {i}')
plt.legend()
plt.xlabel('logmass')
plt.ylabel('Frequency')
plt.title('Subpopulations based on logmass')
plt.savefig('subpopulations.png')
plt.close()


# Plot histograms for 'z' (redshift)
plt.figure(figsize=(10, 6))
for i in range(optimal_n):
    subset = df[df['subpopulation'] == i]
    plt.hist(subset['z'], bins=30, alpha=0.5, label=f'Subpop {i}')
plt.legend()
plt.xlabel('Redshift (z)')
plt.ylabel('Frequency')
plt.title('Redshift Distribution by Subpopulation')
plt.savefig('z_distributions.png')
plt.close()


# Plot histograms for 'sfr' (star formation rate)
plt.figure(figsize=(10, 6))
for i in range(optimal_n):
    subset = df[df['subpopulation'] == i]
    plt.hist(subset['sfr'], bins=30, alpha=0.5, label=f'Subpop {i}')
plt.legend()
plt.xlabel('Star Formation Rate (sfr)')
plt.ylabel('Frequency')
plt.title('Star Formation Rate Distribution by Subpopulation')
plt.savefig('sfr_distributions.png')
plt.close()
