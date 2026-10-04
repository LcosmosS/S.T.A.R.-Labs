import pandas as pd


# Load the CSV data (replace 'galaxy_zoo_data.csv' with the actual file name)
df = pd.read_csv('galaxy_zoo_data.csv')


# Display the first few rows
print(df.head())


# Clean the data (e.g., remove missing values, filter by conditions)
df_cleaned = df.dropna()  # Remove rows with missing values


# Filter for galaxies with specific morphological types (e.g., spirals)
df_filtered = df_cleaned[df_cleaned['morphology'] == 'spiral']


# You can also filter by redshift if needed (e.g., 0.05 < z < 0.1)
df_filtered = df_filtered[(df_filtered['redshift'] > 0.05) & (df_filtered['redshift'] < 0.1)]


# Now, df_filtered has galaxies that match your criteria.
print(df_filtered.head())


# Proceed with analysis or use it to train your model
