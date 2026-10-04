import pandas as pd
df_mytable = pd.read_csv('MyTable_pmqr771.csv')
df_gema = pd.read_csv('GEMA_2.csv')
df_mangahi = pd.read_csv('mangaHIall.csv')
df_pipe3d = pd.read_csv('pipe3d_data2.csv')
print("Columns in MyTable_pmqr771.csv:", df_mytable.columns)
print("Columns in GEMA_2.csv:", df_gema.columns)
print("Columns in mangaHIall.csv:", df_mangahi.columns)
* print("Columns in pipe3d_data2.csv:", df_pipe3d.columns)
