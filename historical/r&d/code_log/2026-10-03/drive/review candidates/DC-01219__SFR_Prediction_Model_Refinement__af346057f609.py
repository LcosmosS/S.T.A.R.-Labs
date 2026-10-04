import pandas as pd


# Load the CSV data
df = pd.read_csv('sdss_galaxies.csv')


# Display the first few rows
print(df.head())


# Drop rows with missing values
df_cleaned = df.dropna()


# Filter for galaxies with stellar mass > 9 and SFR > 0
df_filtered = df_cleaned[(df_cleaned['log_Mass'] > 9) & (df_cleaned['sfr'] > 0)]


# Display the cleaned dataset
print(df_filtered.head())
