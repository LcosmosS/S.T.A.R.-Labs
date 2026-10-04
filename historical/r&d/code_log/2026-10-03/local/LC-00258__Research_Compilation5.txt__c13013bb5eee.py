import pandas as pd
import numpy as np
from sklearn.mixture import GaussianMixture
import matplotlib.pyplot as plt


# Step 1: Subpopulation Identification
# Load and clean data
df = pd.DataFrame({'log_mass': log_mass})  # Replace with actual data
Q1 = df['log_mass'].quantile(0.25)
Q3 = df['log_mass'].quantile(0.75)
IQR = Q3 - Q1
lower_bound = Q1 - 3 * IQR
upper_bound = Q3 + 3 * IQR
df_filtered = df[(df['log_mass'] >= lower_bound) & (df['log_mass'] <= upper_bound)]
log_mass_filtered = df_filtered['log_mass'].values


# Fit GMM
X = log_mass_filtered.reshape(-1, 1)
n_components_range = range(1, 11)
bic_scores = []
models = []
for n in n_components_range:
    gmm = GaussianMixture(n_components=n, random_state=42)
    gmm.fit(X)
    bic_scores.append(gmm.bic(X))
    models.append(gmm)


optimal_n = n_components_range[np.argmin(bic_scores)]
best_gmm = models[np.argmin(bic_scores)]
labels = best_gmm.predict(X)
df_filtered['subpopulation'] = labels


# Visualize
plt.hist(log_mass_filtered, bins=50, alpha=0.5, label='All Data')
for i in range(optimal_n):
    plt.hist(log_mass_filtered[labels == i], bins=50, alpha=0.5, label=f'Subpopulation {i}')
plt.xlabel('log_mass')
plt.ylabel('Frequency')
plt.title('Galaxy Subpopulations Based on Stellar Mass')
plt.legend()
plt.show()


# Step 2: Compute Normalization for Subpopulations
df_filtered['mass'] = 10 ** df_filtered['log_mass']
K_values = []
for i in range(optimal_n):
    subpopulation = df_filtered[df_filtered['subpopulation'] == i]
    masses = subpopulation['mass'].values
    M_0 = np.median(masses)
    sum_M_over_M0 = np.sum(masses / M_0)
    sum_M0_over_M = np.sum(M_0 / masses)
    K = sum_M_over_M0 / sum_M0_over_M
    K_values.append(K)
    print(f"Subpopulation {i}: M_0 = {M_0:.2e}, K = {K:.4f}")


# Step 3: Define Rank
rank = sum(1 for K in K_values if abs(K - 1) <= 0.1)
print(f"Rank (number of subpopulations with K ≈ 1): {rank}")


# Step 4: Refine L-Function Definition
def L_k(s, masses, M_0):
    return np.sum((M_0 / masses) ** s)


L_values = []
for i in range(optimal_n):
    subpopulation = df_filtered[df_filtered['subpopulation'] == i]
    masses = subpopulation['mass'].values
    M_0 = np.median(masses)
    L = L_k(1, masses, M_0)
    L_values.append(L)
    print(f"Subpopulation {i}: L_k(1) = {L:.4f}")


L_cosmo = np.prod(L_values)
print(f"L_cosmo(1) = {L_cosmo:.4f}")
