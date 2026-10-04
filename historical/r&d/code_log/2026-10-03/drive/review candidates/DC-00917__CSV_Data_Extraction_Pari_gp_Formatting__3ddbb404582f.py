import pandas as pd
import numpy as np
from sklearn.mixture import GaussianMixture


# Load the data
df = pd.read_csv('Stellar_Mass2_Table.csv')


# Remove rows where 'logmass' is NaN
df_clean = df.dropna(subset=['logmass'])


# Extract the cleaned 'logmass' data
logmass = df_clean['logmass'].values


# Fit the GMM on the cleaned data
gmm = GaussianMixture(n_components=5, random_state=0).fit(logmass.reshape(-1, 1))
groups = gmm.predict(logmass.reshape(-1, 1))


print("GMM fitting completed successfully.")
