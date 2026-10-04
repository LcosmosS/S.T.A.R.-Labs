from sklearn.mixture import GaussianMixture


X = df['logmass'].values.reshape(-1, 1)
gmm = GaussianMixture(n_components=5, random_state=42)
gmm.fit(X)
df['subpopulation'] = gmm.predict(X)
* print("Optimal number of components: 5")
