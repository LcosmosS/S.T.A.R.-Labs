import pandas as pd


# Load the CSV file
df = pd.read_csv('Stellar_Mass2_Table.csv')


# Filter rows where z and logmass are not -9999
valid_df = df[(df['z'] != -9999) & (df['logmass'] != -9999)]


# Select the first 1000 rows
first_1000 = valid_df.head(1000)


# Check if there are at least 1000 rows
if len(first_1000) < 1000:
    print(f"Warning: Only {len(first_1000)} valid rows found.")


# Extract z and logmass values
z_values = first_1000['z'].tolist()
logmass_values = first_1000['logmass'].tolist()


# Print the lists enclosed in brackets
print("z values: [" + ','.join(map(str, z_values)) + "]")
print("logmass values: [" + ','.join(map(str, logmass_values)) + "]")
