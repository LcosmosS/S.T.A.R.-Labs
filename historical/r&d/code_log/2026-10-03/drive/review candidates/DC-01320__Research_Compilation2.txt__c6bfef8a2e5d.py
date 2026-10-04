# /home/user/cosmology/preprocess.py
import pandas as pd
df = pd.read_csv('/home/user/cosmology/Stellar_Mass2_Table.csv')
df = df[df['logmass'] != -9999]
