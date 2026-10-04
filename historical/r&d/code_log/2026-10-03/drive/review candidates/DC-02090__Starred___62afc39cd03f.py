import pandas as pd
df = pd.read_csv('Stellar_Mass2_Table.csv') key_columns = ['ra', 'dec', 'z', 'logmass', 'sfr'] valid_df = df[df[key_columns].notna().all(axis=1) & (df[key_columns] != -9999.0).all(axis=1)]
