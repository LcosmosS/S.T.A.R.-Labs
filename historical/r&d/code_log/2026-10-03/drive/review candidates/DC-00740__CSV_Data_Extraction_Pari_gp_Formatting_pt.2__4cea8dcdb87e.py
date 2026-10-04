import pandas as pd


df_mytable = pd.read_csv('MyTable_pmqr771.csv')
df_gema = pd.read_csv('GEMA_2.csv')
df_mangahi = pd.read_csv('mangaHIall.csv')
df_pipe3d = pd.read_csv('pipe3d_data2.csv')


df_mytable['mangaid'] = df_mytable['mangaid'].astype(str)
df_gema['mangaid'] = df_gema['mangaid'].astype(str)
df_mangahi['MANGADID'] = df_mangahi['MANGADID'].astype(str)
df_pipe3d['mangaid'] = df_pipe3d['mangaid'].astype(str)


df = df_mytable.merge(df_gema, on='mangaid', how='left')
df = df.merge(df_mangahi, left_on='mangaid', right_on='MANGADID', how='left')
df = df.drop(columns=['MANGADID'], errors='ignore')
df = df.merge(df_pipe3d, on='mangaid', how='left')


df.to_csv('merged_data.csv', index=False)
