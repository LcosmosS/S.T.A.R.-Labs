import pandas as pd
import csv


# Read the CSV files
df_mytable = pd.read_csv('MyTable_pmqr771.csv')
df_gema = pd.read_csv('GEMA_2.csv')
df_mangahi = pd.read_csv('mangaHIall.csv')
df_pipe3d = pd.read_csv('pipe3d_data2.csv')


# Strip spaces from column names to handle leading/trailing spaces
df_mytable.columns = df_mytable.columns.str.strip()
df_gema.columns = df_gema.columns.str.strip()
df_mangahi.columns = df_mangahi.columns.str.strip()
df_pipe3d.columns = df_pipe3d.columns.str.strip()


# Print columns for debugging
print("Columns in MyTable_pmqr771.csv:", df_mytable.columns.tolist())
print("Columns in GEMA_2.csv:", df_gema.columns.tolist())
print("Columns in mangaHIall.csv:", df_mangahi.columns.tolist())
print("Columns in pipe3d_data2.csv:", df_pipe3d.columns.tolist())


# Check for 'mangaid' in all DataFrames, except mangaHIall.csv where we look for 'MANGID'
if 'mangaid' not in df_mytable.columns:
    print("Error: 'mangaid' not in MyTable_pmqr771.csv")
elif 'mangaid' not in df_gema.columns:
    print("Error: 'mangaid' not in GEMA_2.csv")
elif 'mangaid' not in df_pipe3d.columns:
    print("Error: 'mangaid' not in pipe3d_data2.csv")
elif 'MANGID' not in df_mangahi.columns:
    print("Error: 'MANGID' not in mangaHIall.csv, please check column names")
    # Look for similar names
