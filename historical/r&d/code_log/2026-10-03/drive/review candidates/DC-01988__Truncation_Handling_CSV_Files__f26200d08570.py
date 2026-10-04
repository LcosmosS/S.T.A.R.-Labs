import pandas as pd
pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.max_colwidth', -1)
pd.set_option('display.width', None)
df = pd.read_csv('Stellar_Mass2_Table.csv')
valid_df = df[(df != -9999).all(axis=1)]  # Filter out rows with -9999
print(valid_df)
