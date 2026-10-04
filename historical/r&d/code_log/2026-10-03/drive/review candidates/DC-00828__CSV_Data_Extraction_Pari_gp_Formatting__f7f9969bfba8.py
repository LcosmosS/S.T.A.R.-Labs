from sklearn.mixture import GaussianMixture
import numpy as np


# Assuming logmass is a numpy array
logmass = np.array(logmass)  # Convert to numpy array if necessary


# Fit GMM with, say, 3 components
gmm = GaussianMixture(n_components=3, random_state=0).fit(logmass.reshape(-1, 1))


# Predict the component for each galaxy
components = gmm.predict(logmass.reshape(-1, 1))


# For each component, compute K_theory
for i in range(3):
    logmass_comp = logmass[components == i]
    # Compute K_theory for this component using your function
    K_comp = compute_K_theory(logmass_comp)
    print(f"Component {i}: K_theory = {K_comp}")
