from sklearn.mixture import GaussianMixture
import numpy as np


logmass = df['logmass'].values.reshape(-1, 1)
n_components_range = range(1, 11)
bic_scores = []
models = []


for n in n_components_range:
    gmm = GaussianMixture(n_components=n, random_state=42)
    gmm.fit(logmass)
    bic_scores.append(gmm.bic(logmass))
    models.append(gmm)


optimal_n = n_components_range[np.argmin(bic_scores)]
best_gmm = models[np.argmin(bic_scores)]
print(f"Optimal number of components: {optimal_n}")
