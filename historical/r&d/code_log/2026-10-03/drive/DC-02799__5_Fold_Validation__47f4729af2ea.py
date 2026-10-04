import pandas as pd df = pd.read_csv('Filtered_Pipe3D.csv') X = df.drop(columns=['log_SFR_Ha']) # Features (all columns except the target) y = df['log_SFR_Ha'] # Target (SFR)
