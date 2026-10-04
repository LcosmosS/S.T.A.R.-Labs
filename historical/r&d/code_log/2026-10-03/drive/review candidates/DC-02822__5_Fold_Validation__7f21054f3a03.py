X = df.drop(columns=['log_SFR_Ha']) # Features (all columns except log_SFR_Ha) y = df['log_SFR_Ha'] # Target (log_SFR_Ha)
from sklearn.model_selection import train_test_split
