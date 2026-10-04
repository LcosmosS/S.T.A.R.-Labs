import pandas as pd
import numpy as np
from sklearn.mixture import GaussianMixture


df = pd.read_csv('Stellar_Mass2_Table.csv')
logmass = df['logmass'].values.reshape(-1, 1)
gmm = GaussianMixture(n_components=5, random_state=0)
groups = gmm.fit_predict(logmass)


np.save('/home/pmqr7/groups.npy', groups)
np.save('/home/pmqr7/z.npy', df['z'].values)
np.save('/home/pmqr7/sfr.npy', df['sfr'].values)
np.save('/home/pmqr7/ra.npy', df['ra'].values)
np.save('/home/pmqr7/dec.npy', df['dec'].values)
np.save('/home/pmqr7/logmass.npy', df['logmass'].values)
