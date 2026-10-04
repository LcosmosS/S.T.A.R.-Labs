import pandas as pd


# Load the datasets
GEMA_2 = pd.read_csv('GEMA_2.csv')
pipe3d_data2 = pd.read_csv('pipe3d_data2.csv')
mangaHIall = pd.read_csv('mangaHIall.csv')


# Rename 'MANGAID' to 'mangaid' in mangaHIall
mangaHIall = mangaHIall.rename(columns={'MANGAID': 'mangaid'})


# Merge the datasets using 'mangaid'
merged_data = pd.merge(GEMA_2, mangaHIall, on='mangaid', how='inner')
final_merged_data = pd.merge(merged_data, pipe3d_data2, on='mangaid', how='inner')


# Save the result
final_merged_data.to_csv('complete_galaxy_dataset.csv', index=False)
