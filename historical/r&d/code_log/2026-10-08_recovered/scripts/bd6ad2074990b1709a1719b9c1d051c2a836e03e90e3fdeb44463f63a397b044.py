import pandas as pd

# Path to the dataset
sdss_data_path = 'SDSSDR18_200000.csv'  # Replace with the correct path

# Load the dataset
df_sdss = pd.read_csv(sdss_data_path)

# Show the first few rows of the dataframe to inspect the data
print("First 5 rows of the dataset:")
print(df_sdss.head())

# Show the column names to confirm they match the expected structure
print("\nColumn names:")
print(df_sdss.columns)

# Basic statistics for numeric columns
print("\nBasic statistics for numeric columns:")
print(df_sdss.describe())

# Check for missing values
print("\nMissing values in the dataset:")
print(df_sdss.isnull().sum())
