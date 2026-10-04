import pandas as pd


# Read the CSV file
df = pd.read_csv('Stellar_Mass2_Table.csv')


# Extract the 'logmass' column (assumed to be in log10 solar masses)
logmasses = df['logmass']


# Convert to linear masses, filtering out invalid entries (e.g., -9999)
