import pandas as pd
df = pd.read_csv('Stellar_Mass2_Table.csv')
df = df[df['logmass'] != -9999]  # Filter invalid masses
