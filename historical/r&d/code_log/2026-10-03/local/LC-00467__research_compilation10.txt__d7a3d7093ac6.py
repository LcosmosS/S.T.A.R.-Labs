import pandas as pd


# Load the datasets
GEMA_2 = pd.read_csv('GEMA_2.csv')
pipe3d_data2 = pd.read_csv('pipe3d_data2.csv')
mangaHIall = pd.read_csv('mangaHIall.csv')


# Merge GEMA_2 and mangaHIall, accounting for different column names
merged_data = pd.merge(GEMA_2, mangaHIall, left_on='mangaid', right_on='MANGAID', how='inner')


# Drop the redundant 'MANGAID' column
merged_data = merged_data.drop(columns=['MANGAID'])


# Merge with pipe3d_data2
final_merged_data = pd.merge(merged_data, pipe3d_data2, on='mangaid', how='inner')


# Save the result
final_merged_data.to_csv('complete_galaxy_dataset.csv', index=False)
