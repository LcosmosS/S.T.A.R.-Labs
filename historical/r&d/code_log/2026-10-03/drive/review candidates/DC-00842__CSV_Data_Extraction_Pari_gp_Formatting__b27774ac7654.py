import pandas as pd


# Load the CSV file
df = pd.read_csv('Stellar_Mass2_Table.csv')


# Define key columns to process
key_columns = ['ra', 'dec', 'z', 'logmass', 'sfr', 'petrorad_r', 'ellipticity']


# Filter out rows with missing values or -9999.0 (invalid entries)
valid_df = df[df[key_columns].notna().all(axis=1) & (df[key_columns] != -9999.0).all(axis=1)]
