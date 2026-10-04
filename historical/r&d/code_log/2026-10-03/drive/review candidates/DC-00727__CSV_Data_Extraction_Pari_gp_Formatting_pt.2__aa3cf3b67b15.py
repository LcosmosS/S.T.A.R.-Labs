import pandas as pd
import csv


# Load the CSV files
df_mytable = pd.read_csv('MyTable.csv')
df_gema2 = pd.read_csv('GEMA2.csv')
df_mangahi = pd.read_csv('MangaHIall.csv')
df_pipe3d = pd.read_csv('Pipe3D.csv')


# Ensure mangaid is string type for consistency
df_mytable['mangaid'] = df_mytable['mangaid'].astype(str)
df_gema2['mangaid'] = df_gema2['mangaid'].astype(str)
df_mangahi['mangaid'] = df_mangahi['mangaid'].astype(str)
df_pipe3d['mangaid'] = df_pipe3d['mangaid'].astype(str)


# Merge the DataFrames, assuming 'mangaid' is the common column
merged_df = df_mytable.merge(df_gema2, on='mangaid', how='left')
merged_df = merged_df.merge(df_mangahi, on='mangaid', how='left')
merged_df = merged_df.merge(df_pipe3d, on='mangaid', how='left')


# Save the merged result
merged_df.to_csv('merged_table.csv', index=False, quoting=csv.QUOTE_ALL)


# Optional: Print to verify
print(f"Final merged DataFrame shape: {merged_df.shape}")
