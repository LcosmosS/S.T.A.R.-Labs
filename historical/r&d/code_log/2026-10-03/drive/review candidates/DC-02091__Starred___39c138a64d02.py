import pandas as pd


# Read the CSV file
df = pd.read_csv('Stellar_Mass2_Table.csv')


# Define the key columns to filter and include in the output
key_columns = ['ra', 'dec', 'z', 'logmass', 'sfr']


# Filter rows where all key columns are not NaN and not -9999.0
valid_df = df[df[key_columns].notna().all(axis=1) & (df[key_columns] != -9999.0).all(axis=1)]


# Create formatted strings for only the specified columns
formatted_list = []
for col in key_columns:
    values_str = ','.join(valid_df[col].astype(str))
    formatted = f"{col}=[{values_str}];"
    formatted_list.append(formatted)


# Combine all formatted strings with newlines
output = '\n'.join(formatted_list)


# Save to file
with open('STM_Extract_Valid.gp', 'w') as f:
    f.write(output)
