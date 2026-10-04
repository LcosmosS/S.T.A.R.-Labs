import pandas as pd
import csv


# Read the CSV files
df_mytable = pd.read_csv('MyTable.csv')
df_gema2 = pd.read_csv('GEMA2.csv')
df_mangahi = pd.read_csv('MangaHIall.csv')
df_pipe3d = pd.read_csv('Pipe3D.csv')


# Perform the joins, starting with MyTable as the base (15,000 rows, already filtered)
df = df_mytable.copy()


# Left join with GEMA2 on mangaid, to add halo mass data
df = df.merge(df_gema2, on='mangaid', how='left')


# Left join with MangaHIall on mangaid, to add HI density data
df = df.merge(df_mangahi, on='mangaid', how='left')


# Left join with Pipe3D on mangaid, to add stellar population or emission line data
df = df.merge(df_pipe3d, on='mangaid', how='left')


# Since MyTable is already 15,000 rows, no need for TOP, but ensure filters
# Assuming nsa_z and nsa_sersic_mass are in df_mytable and already filtered
df = df[df['nsa_z'].notnull() & df['nsa_sersic_mass'].notnull()]


# If daptype is in MyTable and needs filtering (though likely already done)
if 'daptype' in df.columns:
    df = df[df['daptype'] == 'HYB10-MILESHC-MASTARSSP']


# Select specific columns, assuming they exist and match the query
columns_to_select = [
    'mangaid', 'nsa_sersic_mass', 'nsa_z', 'OBJDEC', 'objra',
    'SFR_PETRORAD_R', 'nsa_loghiidens', 'nsa_logohidens', 'nsa_halo_mass'
]
df = df[columns_to_select]


# Save the result to a new CSV
df.to_csv('joined_data.csv', index=False, quoting=csv.QUOTE_ALL)


# Optional: Print to verify
print(f"Final merged DataFrame shape: {df.shape}")
print(f"Number of rows: {len(df)}")
