import pandas as pd
# Load the CSV file
df = pd.read_csv('Stellar_Mass2_Table.csv')
# Filter rows where z and logmass are not -9999
valid_df = df[(df['z'] != -9999) & (df['logmass'] != -9999)]
# Select the first 9214 valid rows
selected_df = valid_df.head(9214)
# Check if there are at least 9214 valid rows
