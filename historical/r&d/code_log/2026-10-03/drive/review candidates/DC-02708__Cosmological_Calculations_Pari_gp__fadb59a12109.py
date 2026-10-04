import pandas as pd


# Load the CSV file
df = pd.read_csv('Stellar_Mass2_Table.csv')


# Filter rows where z and logmass are not -9999
valid_df = df[(df['z'] != -9999) & (df['logmass'] != -9999)]


# Select the first 9214 valid rows
selected_df = valid_df.head(9214)


# Check if there are at least 9214 valid rows
if len(selected_df) < 9214:
    print(f"Warning: Only {len(selected_df)} valid rows found, less than 9214.")


# Extract z and logmass values
z_values = selected_df['z'].tolist()
logmass_values = selected_df['logmass'].tolist()


# Print the number of selected rows
print(f"Number of selected rows: {len(selected_df)}")


# Print the lists enclosed in brackets
print("z values: [" + ','.join(map(str, z_values)) + "]")
print("logmass values: [" + ','.join(map(str, logmass_values)) + "]")
