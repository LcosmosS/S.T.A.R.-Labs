import pandas as pd


# Read the CSV files
df_mytable = pd.read_csv('MyTable.csv')
df_gema2 = pd.read_csv('GEMA2.csv')
df_mangahi = pd.read_csv('MangaHIall.csv')
df_pipe3d = pd.read_csv('Pipe3D.csv')


# Perform the joins, starting with MyTable as the base
# Assuming MyTable already has data from mangaDrpAll and mangaDapAll joined
df = df_mytable.copy()


# Left join with GEMA2 on mangaid
df = df.merge(df_gema2, on='mangaid', how='left')


# Left join with MangaHIall on mangaid
df = df.merge(df_mangahi, on='mangaid', how='left')


# Left join with Pipe3D on mangaid
df = df.merge(df_pipe3d, on='mangaid', how='left')


# Apply filters similar to the SQL query
# Assuming nsa_z and nsa_sersic_mass are in df_mytable
df = df[df['nsa_z'].notnull() & df['nsa_sersic_mass'].notnull()]


# If daptype is in MyTable and needs filtering
if 'daptype' in df.columns:
    df = df[df['daptype'] == 'HYB10-MILESHC-MASTARSSP']


# Select specific columns, assuming they exist
columns_to_select = [
    'mangaid', 'nsa_sersic_mass', 'nsa_z', 'OBJDEC', 'objra',
    'SFR_PETRORAD_R', 'nsa_loghiidens', 'nsa_logohidens', 'nsa_halo_mass'
]
df = df[columns_to_select]


# Limit to top 15000 if needed, though user didn't specify
df = df.head(15000)


# Save the result to a new CSV
df.to_csv('joined_data.csv', index=False)
