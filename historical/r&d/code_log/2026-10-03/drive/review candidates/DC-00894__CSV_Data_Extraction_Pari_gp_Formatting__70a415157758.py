import pandas as pd
import numpy as np
from sklearn.mixture import GaussianMixture


# Load the CSV file
df = pd.read_csv('Stellar_Mass2_Table.csv')


# Assume 'logmass' is the column for clustering
logmass = df['logmass'].values.reshape(-1, 1)


# Fit GMM with, say, 5 components
gmm = GaussianMixture(n_components=5, random_state=0)
groups = gmm.fit_predict(logmass)


# Save the arrays
np.save('groups.npy', groups)
np.save('z.npy', df['z'].values)
np.save('sfr.npy', df['sfr'].values)
np.save('ra.npy', df['ra'].values)
np.save('dec.npy', df['dec'].values)
np.save('logmass.npy', df['logmass'].values)
