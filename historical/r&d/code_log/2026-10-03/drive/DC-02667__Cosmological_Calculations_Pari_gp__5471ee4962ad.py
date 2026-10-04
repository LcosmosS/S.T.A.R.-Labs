import pandas as pd


# Load the CSV file
df = pd.read_csv('Stellar_Mass2_Table.csv')


# Filter rows where z and logmass are not -9999
valid_df = df[(df['z'] != -9999) & (df['logmass'] != -9999)]


# Extract z and logmass values from all valid rows
z_values = valid_df['z'].tolist()
logmass_values = valid_df['logmass'].tolist()


# Print the number of valid rows
print("Number of valid rows: ", len(valid_df))


# Print the lists enclosed in brackets
print("z values: [" + ','.join(map(str, z_values)) + "]")
print("logmass values: [" + ','.join(map(str, logmass_values)) + "]")
