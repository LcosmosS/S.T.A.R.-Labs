import pandas as pd
df = pd.read_csv('Filtered_Pipe3D.csv')
X = df.drop(columns=['log_SFR_Ha'])  # Features
y = df['log_SFR_Ha']  # Target
