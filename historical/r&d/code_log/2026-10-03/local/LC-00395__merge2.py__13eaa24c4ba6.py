import pandas as pd

# Load the CSV files
df1 = pd.read_csv('GZ_410166_2.csv')
df2 = pd.read_csv('GZ_410166.csv')
df3 = pd.read_csv('GZ_gzdv1-2.csv')

# Strip extra spaces in column names
df1.columns = df1.columns.str.strip()
df2.columns = df2.columns.str.strip()
df3.columns = df3.columns.str.strip()

# Check if 'recno' exists in each DataFrame, and if not, create a new one
if 'recno' not in df1.columns:
    print("Creating 'recno' in df1")
    df1['recno'] = range(1, len(df1) + 1)

if 'recno' not in df2.columns:
    print("Creating 'recno' in df2")
    df2['recno'] = range(1, len(df2) + 1)

if 'recno' not in df3.columns:
    print("Creating 'recno' in df3")
    df3['recno'] = range(1, len(df3) + 1)

# Check the first few rows to ensure the 'recno' column is created
print(df1[['recno']].head())
print(df2[['recno']].head())
print(df3[['recno']].head())

# Merge the DataFrames on the new 'recno' column
merged_df = pd.merge(df1, df2, on='recno', how='outer')
merged_df = pd.merge(merged_df, df3, on='recno', how='outer')

# Optionally, check the first few rows of the merged DataFrame
print(merged_df.head())

# Save the merged DataFrame
merged_df.to_csv('merged_output.csv', index=False)
