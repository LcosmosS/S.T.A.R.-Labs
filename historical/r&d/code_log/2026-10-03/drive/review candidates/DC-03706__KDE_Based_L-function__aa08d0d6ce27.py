# Morphology entropy as uncertainty indicator
from scipy.stats import entropy
morph_probs = gz_df[['pE', 'pS', 'pEdg', 'pDK', 'pMg']].fillna(0)
gz_df['morphology_entropy'] = morph_probs.apply(lambda row: entropy(row.values + 1e-6), axis=1)


# Previous feature engineering kept intact
gz_df['morph_sum'] = gz_df[['Smooth', 'Featured']].sum(axis=1)
gz_df['dust_corrected_mag'] = gz_df['rMag'] - gz_df['Ar']
