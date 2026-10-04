from sklearn.mixture import GaussianMixture
import numpy as np


logmass = np.array(your_filtered_logmass_data)  # Your logmass data
gmm = GaussianMixture(n_components=3).fit(logmass.reshape(-1, 1))
