import pandas as pd
df = pd.read_csv('Stellar_Mass2_Bigsby.csv')
valid_df = df[(df != -9999).all(axis=1)]
