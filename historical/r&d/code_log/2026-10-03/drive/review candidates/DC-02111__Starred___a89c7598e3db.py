import pandas as pd


df = pd.read_csv('Stellar_Mass2_Table.csv')
key_columns = ['ra', 'dec', 'z', 'logmass', 'sfr', 'petrorad_r', 'ellipticity', 'objid']
valid_df = df[df[key_columns].notna().all(axis=1) & (df[key_columns] != -9999.0).all(axis=1)]


with open('C:\\temp\\STM_Extract_Valid.gp', 'w') as f:
    for col in key_columns:
        if col == 'objid':
            values = ','.join(f'"{str(val)}"' for val in valid_df[col])  # Strings with quotes
        else:
            values = ','.join(str(val) for val in valid_df[col])  # Numbers without quotes
        f.write(f"{col}=[{values}];\n")
