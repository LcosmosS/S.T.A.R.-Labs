import pandas as pd


# Load and rename mangaHIall
mangaHIall = pd.read_csv('mangaHIall.csv')
mangaHIall = mangaHIall.rename(columns={'MANGAID': 'mangaid'})


# Load other files
GEMA_2 = pd.read_csv('GEMA_2.csv')
pipe3d_data2 = pd.read_csv('pipe3d_data2.csv')


# Merge all datasets
merged_data = pd.merge(GEMA_2, mangaHIall, on='mangaid', how='inner')
final_merged_data = pd.merge(merged_data, pipe3d_data2, on='mangaid', how='inner')


# Optional: Save the result
final_merged_data.to_csv('final_merged_data.csv', index=False)
print("Merge completed successfully!")
