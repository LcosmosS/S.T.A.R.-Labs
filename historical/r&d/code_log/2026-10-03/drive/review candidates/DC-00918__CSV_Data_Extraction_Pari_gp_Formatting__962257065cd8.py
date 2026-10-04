import pandas as pd
import numpy as np
from sklearn.mixture import GaussianMixture
from sklearn.impute import SimpleImputer


# Load the data
df = pd.read_csv('Stellar_Mass2_Table.csv')


# Create an imputer to replace NaN with the mean
imputer = SimpleImputer(strategy='mean')


# Impute NaN values in 'logmass'
logmass_imputed = imputer.fit_transform(df[['logmass']])


# Fit the GMM on the imputed data
gmm = GaussianMixture(n_components=5, random_state=0).fit(logmass_imputed)
groups = gmm.predict(logmass_imputed)


print("GMM fitting completed successfully with imputed data.")
