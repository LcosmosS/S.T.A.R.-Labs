# Normalize both variables
from sklearn.preprocessing import MinMaxScaler scaler = MinMaxScaler() gz_df[['morph_sum_norm', 'Pth100_norm']] = scaler.fit_transform(gz_df[['morph_sum', 'Pth100']])
# Rank idea 1: average of normalized metrics
gz_df['cosmo_rank'] = (gz_df['morph_sum_norm'] + gz_df['Pth100_norm']) / 2
# Rank idea 2: weighted, give more influence to structure or environment
gz_df['cosmo_rank'] = 0.7 * gz_df['Pth100_norm'] + 0.3 * gz_df['morph_sum_norm']
X['cosmo_rank'] = gz_df['cosmo_rank']
