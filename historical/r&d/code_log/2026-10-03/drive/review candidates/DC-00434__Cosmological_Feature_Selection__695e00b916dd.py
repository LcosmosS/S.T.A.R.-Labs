import pandas as pd
from sklearn.preprocessing import MinMaxScaler


# Assume gz_df is your DataFrame with the Galaxy Zoo data
# Calculate morph_sum as sum of morphological probabilities
morph_cols = ['P(CD)', 'P(E)', 'P(S0)', 'P(Sa)', 'P(Sab)', 'P(Sb)', 'P(Sbc)', 
              'P(Sc)', 'P(Scd)', 'P(Sd)', 'P(Sdm)', 'P(Sm)', 'P(Irr)']
gz_df['morph_sum'] = gz_df[morph_cols].sum(axis=1)


# Use conf_prob as Pth100 (or replace with actual Pth100 if defined differently)
gz_df['Pth100'] = gz_df['conf_prob']


# Normalize morph_sum, Pth100, and nsa_z
scaler = MinMaxScaler()
