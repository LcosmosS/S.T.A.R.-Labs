from sklearn.mixture import GaussianMixture import numpy as np
# Load your filtered logmass data (export from PARI/GP if needed)
logmass = np.array(filtered_logmass) # Replace with your data
# Fit GMM with 3 components (adjust as needed)
gmm = GaussianMixture(n_components=3, random_state=0).fit(logmass.reshape(-1, 1))
# Predict components
components = gmm.predict(logmass.reshape(-1, 1))
# Function to compute K_theory (translated from PARI/GP)
def compute_K_theory(logmass_vec): M = 10 ** logmass_vec M_sorted = np.sort(M) n = len(M) if n == 0: return 0 if n % 2 == 1: M0 = M_sorted[n // 2] else: M0 = (M_sorted[n // 2 - 1] + M_sorted[n // 2]) / 2 sum_M_over_M0 = np.sum(M / M0) sum_M0_over_M = np.sum(M0 / M) return sum_M_over_M0 / sum_M0_over_M
# Compute K_theory for each component
for i in range(3): logmass_comp = logmass[components == i] K_comp = compute_K_theory(logmass_comp) print(f"Component {i}: K_theory = {K_comp}")
