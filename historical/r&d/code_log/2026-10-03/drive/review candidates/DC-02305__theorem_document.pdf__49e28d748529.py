import pandas as pd
import numpy as np
def preprocess_galaxy_data(filename):
data = pd.read_csv(filename)
data = data[(data['z'] > 0.01) & (data['z'] < 0.5)]
data['log_mass'] = np.log10(data['stellar_mass'])
data['sfr_norm'] = data['sfr'] / data['stellar_mass']
data = data.dropna()
return data
galaxy_data = preprocess_galaxy_data('sdss_galaxy_data.csv')
