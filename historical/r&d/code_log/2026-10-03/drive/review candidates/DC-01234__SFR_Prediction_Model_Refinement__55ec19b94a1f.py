import pandas as pd


# Load the three CSV files
df1 = pd.read_csv('GZ_410166_2.csv')
df2 = pd.read_csv('GZ_410166.csv')
df3 = pd.read_csv('GZ_gzdv1-2.csv')


# Merge the DataFrames on the 'recno' column
# Using 'outer' merge ensures all rows from all dataframes are kept
merged_df = pd.merge(df1, df2, on='recno', how='outer')
merged_df = pd.merge(merged_df, df3, on='recno', how='outer')


# Fill any missing values with 0 (you can change this to a different value if needed)
merged_df.fillna(0, inplace=True)


# Save the merged DataFrame to a new CSV file
merged_df.to_csv('merged_output.csv', index=False)


# Print the first few rows of the merged data to verify
print(merged_df.head())
