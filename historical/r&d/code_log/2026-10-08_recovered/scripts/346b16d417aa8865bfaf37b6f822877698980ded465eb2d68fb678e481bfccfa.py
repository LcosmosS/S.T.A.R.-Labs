import pandas as pd
import numpy as np

# Load the dataset
csv_file = 'Stellar_Mass2_Table.csv'
try:
    df = pd.read_csv(csv_file)
except FileNotFoundError:
    print(f"Error: '{csv_file}' not found.")
    exit(1)

# Define invalid value
invalid_value = -9999.0

# Exclude 'metallicity' and 'objid' columns
columns_to_keep = [col for col in df.columns if col not in ['metallicity', 'objid']]
df_filtered = df[columns_to_keep].copy()

# Remove rows with invalid values
df_filtered.replace(invalid_value, np.nan, inplace=True)
df_cleaned = df_filtered.dropna()

# Save the cleaned data to a new CSV file
output_file = 'Stellar_Mass2_Table_cleaned.csv'
df_cleaned.to_csv(output_file, index=False)
print(f"Cleaned data saved to '{output_file}'.")