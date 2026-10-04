bic = []
for n in range(2, 6):
    temp_gmm = GaussianMixture(n_components=n, random_state=0).fit(logmass.reshape(-1, 1))
    bic.append(temp_gmm.bic(logmass.reshape(-1, 1)))
optimal_n = np.argmin(bic) + 2
print(f"Optimal number of components based on BIC: {optimal_n}")
gmm = GaussianMixture(n_components=optimal_n, random_state=0).fit(logmass.reshape(-1, 1))
groups = gmm.predict(logmass.reshape(-1, 1))
