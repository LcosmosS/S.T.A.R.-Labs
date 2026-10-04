import pandas as pd
import csv


# Read the large CSV file
df = pd.read_csv('pipe3d_data.csv')


# Get total number of rows
total_rows = len(df)


# Number of files to split into
num_files = 4


# Calculate rows per file
rows_per_file = total_rows // num_files


# Split and write to separate CSV files
for i in range(num_files):
    start = i * rows_per_file
    if i < num_files - 1:
        end = (i + 1) * rows_per_file
    else:
        end = total_rows
    df_part = df.iloc[start:end]
    df_part.to_csv(f'pipe3d_data_part{i+1}.csv', index=False, quoting=csv.QUOTE_ALL)
    print(f"File {i+1}: rows {start} to {end-1}, total {len(df_part)} rows")
