import pandas as pd


# Read the CSV file
df = pd.read_csv('Stellar_Mass2_Table.csv')


# Filter rows where z and logmass are not -9999
valid_df = df[(df['z'] != -9999) & (df['logmass'] != -9999)]


# Select the first 1000 rows
first_1000 = valid_df.head(1000)


# Extract z and logmass values
z_values = first_1000['z'].tolist()
logmass_values = first_1000['logmass'].tolist()


# Print the lists
print("First 1000 valid z values:")
print(','.join(map(str, z_values)))
print("\nFirst 1000 valid log_mass values:")
print(','.join(map(str, logmass_values)))
