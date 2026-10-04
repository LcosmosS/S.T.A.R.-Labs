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


# Extract logmass values
logmass_values = selected_df['logmass'].tolist()


# Save to data_extract.txt in PARI/GP format
with open('C:\\temp\\data_extract.txt', 'w') as f:
    f.write("log_mass = [" + ','.join(map(str, logmass_values)) + "];")


print("Data saved to C:\\temp\\data_extract.txt")
