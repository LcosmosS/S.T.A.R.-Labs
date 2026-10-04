import pandas as pd


df = pd.read_csv('Stellar_Mass2_Table.csv')
key_columns = ['ra', 'dec', 'z', 'logmass', 'sfr']
valid_df = df[df[key_columns].notna().all(axis=1) & (df[key_columns] != -9999.0).all(axis=1)]


include_columns = ['objid', 'ra', 'dec', 'z', 'logmass', 'petrorad_r', 'ellipticity', 'sfr']
formatted_list = []
for col in include_columns:
    values_str = ','.join(valid_df[col].astype(str))
    formatted = f"{col}=[{values_str}];"
    formatted_list.append(formatted)


output = '\n'.join(formatted_list)
with open('STM_Extract_Valid.gp', 'w') as f:
    f.write(output)
