import pandas as pd


df = pd.read_csv('Stellar_Mass2_Table.csv')
key_columns = ['ra', 'dec', 'z', 'logmass', 'sfr', 'petrorad_r', 'ellipticity', 'objid']
valid_df = df[df[key_columns].notna().all(axis=1) & (df[key_columns] != -9999.0).all(axis=1)]


with open('C:\\temp\\STM_Extract_Valid.gp', 'w') as f:
    for col in key_columns:
        values = ','.join(valid_df[col].astype(str))
