import pandas as pd
import numpy as np
from sklearn.mixture import GaussianMixture
import matplotlib.pyplot as plt


# Load the CSV file
df = pd.read_csv('Stellar_Mass2_Table.csv')


# Extract relevant columns
z = df['z'].values
sfr = df['sfr'].values
ra = df['ra'].values
dec = df['dec'].values
logmass = df['logmass'].values


# Fit GMM to logmass
gmm = GaussianMixture(n_components=5, random_state=0)
groups = gmm.fit_predict(logmass.reshape(-1, 1))


# Now proceed with the analysis
# ... (rest of the script)
