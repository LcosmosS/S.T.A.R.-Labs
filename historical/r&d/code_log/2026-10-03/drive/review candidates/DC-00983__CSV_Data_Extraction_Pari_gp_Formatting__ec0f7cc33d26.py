import pandas as pd import numpy as np
# Load data
df = pd.read_csv("Stellar_Mass2_Table_cleaned.csv") print("Loaded data successfully.") print("Available columns:", df.columns.tolist())
# Define column names based on your dataset
logmass_col = 'logmass' # Logarithmic stellar mass z_col = 'z' # Redshift property_col = 'sfr' # Example: using star formation rate as a property
# Check for missing columns
