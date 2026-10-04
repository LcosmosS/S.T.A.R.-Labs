import pandas as pd import numpy as np import matplotlib.pyplot as plt from sklearn.metrics import mean_squared_error
# Load the data
df = pd.read_csv("Stellar_Mass2_Table_cleaned.csv") print("Loaded data successfully.")
# Define column names for readability
logmass_col = 'logmass' # Logarithmic stellar mass z_col = 'z' # Redshift sfr_col = 'sfr' # Star formation rate
# Handle missing values by imputing with the mean
