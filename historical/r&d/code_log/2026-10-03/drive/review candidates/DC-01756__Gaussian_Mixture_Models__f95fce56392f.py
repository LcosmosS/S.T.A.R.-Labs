# Prepare the data for GMM (reshape for sklearn)
X = log_mass_filtered.reshape(-1, 1)


# Test different numbers of components to find the optimal number using BIC
n_components_range = range(1, 11)
bic_scores = []
models = []


for n in n_components_range:
    gmm = GaussianMixture(n_components=n, random_state=42)
    gmm.fit(X)
    bic_scores.append(gmm.bic(X))
    models.append(gmm)


# Find the number of components with the lowest BIC
optimal_n = n_components_range[np.argmin(bic_scores)]
best_gmm = models[np.argmin(bic_scores)]


print(f"Optimal number of components: {optimal_n}")


# Plot BIC scores
plt.plot(n_components_range, bic_scores, marker='o')
plt.xlabel('Number of Components')
plt.ylabel('BIC Score')
plt.title('BIC Score vs. Number of Components')
7. plt.show()
