import pandas as pd
import numpy as np
from sklearn.mixture import GaussianMixture


# Load the data
df = pd.read_csv('Stellar_Mass2_Table.csv')


# Remove rows with NaN in 'logmass'
df_clean = df.dropna(subset=['logmass'])


# Extract cleaned data (adjust column names as needed)
z = df_clean['z'].values
sfr = df_clean['sfr'].values
ra = df_clean['ra'].values
dec = df_clean['dec'].values
logmass = df_clean['logmass'].values


# Fit GMM on cleaned logmass
gmm = GaussianMixture(n_components=5, random_state=0).fit(logmass.reshape(-1, 1))
groups = gmm.predict(logmass.reshape(-1, 1))


print("GMM fitting completed successfully.")
# Continue with your analysis...
