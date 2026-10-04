import pandas as pd
import csv


# Read the CSV files
df_mytable = pd.read_csv('MyTable_pmqr771.csv')
df_gema = pd.read_csv('GEMA_2.csv')
df_mangahi = pd.read_csv('mangaHIall.csv')
df_pipe3d = pd.read_csv('pipe3d_data2.csv')


# Ensure 'mangaid' is present in all DataFrames for joining
if 'mangaid' not in df_mytable.columns:
    print("Error: 'mangaid' not in MyTable_pmqr771.csv")
elif 'mangaid' not in df_gema.columns:
    print("Error: 'mangaid' not in GEMA_2.csv")
elif 'mangaid' not in df_mangahi.columns:
    print("Error: 'mangaid' not in mangaHIall.csv")
elif 'mangaid' not in df_pipe3d.columns:
    print("Error: 'mangaid' not in pipe3d_data2.csv")
else:
    # Ensure 'mangaid' is string type for consistency
    df_mytable['mangaid'] = df_mytable['mangaid'].astype(str)
    df_gema['mangaid'] = df_gema['mangaid'].astype(str)
    df_mangahi['mangaid'] = df_mangahi['mangaid'].astype(str)
    df_pipe3d['mangaid'] = df_pipe3d['mangaid'].astype(str)


    # Perform left merges on 'mangaid', starting with MyTable as base
    df = df_mytable.merge(df_gema, on='mangaid', how='left')
    df = df.merge(df_mangahi, on='mangaid', how='left')
    df = df.merge(df_pipe3d, on='mangaid', how='left')


    # Save the merged result with all fields quoted for compatibility
    df.to_csv('merged_data.csv', index=False, quoting=csv.QUOTE_ALL)
    print("Merged data saved to merged_data.csv with all fields quoted")
