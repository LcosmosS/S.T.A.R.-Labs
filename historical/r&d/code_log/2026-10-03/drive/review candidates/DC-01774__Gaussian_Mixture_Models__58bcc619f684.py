from sklearn.mixture import GaussianMixture
import numpy as np


# Extract logmass
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


# Update PARI/GP script output columns
output_columns = ['mass', 'subpopulation', 'objid', 'ra', 'dec', 'z', 'logmass', 'petrorad_r', 'ellipticity', 'sfr', 'metallicity']
