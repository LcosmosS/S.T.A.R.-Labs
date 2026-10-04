from sklearn.mixture import GaussianMixture
n_components_range = range(1, 11)
bic = []
for n in n_components_range:
    gmm = GaussianMixture(n_components=n, random_state=42)
    gmm.fit(X)
    bic.append(gmm.bic(X))
optimal_n = n_components_range[np.argmin(bic)]
