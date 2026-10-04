import pandas as pd
import numpy as np
from sklearn.mixture import GaussianMixture
import matplotlib.pyplot as plt


# Load your data (adjust path as needed)
df = pd.read_csv('your_data.csv')


# Filter out non-positive logmass values
df = df[df['logmass'] > 0]
print(f"Rows after filtering: {len(df)}")


# Fit GMM to logmass
X = df['logmass'].values.reshape(-1, 1)
gmm = GaussianMixture(n_components=5, random_state=42)
gmm.fit(X)
labels = gmm.predict(X)
df['subpopulation'] = labels


# Compute masses and K for each subpopulation
for i in range(5):
    masses = 10 ** df[df['subpopulation'] == i]['logmass']
    M0 = np.median(masses)
    sum_M_over_M0 = np.sum(masses / M0)
    sum_M0_over_M = np.sum(M0 / masses)
    K = (sum_M_over_M0 * sum_M0_over_M) ** 0.5  # Adjust formula if needed
    print(f"Subpopulation {i}: M0 = {M0:.2e}, K = {K:.4f}")


# Compute rank with threshold 0.2
threshold = 0.2
