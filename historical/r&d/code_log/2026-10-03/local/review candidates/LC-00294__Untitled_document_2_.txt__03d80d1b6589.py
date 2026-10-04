X = df.drop(columns=['log_SFR_Ha']) # Features y = df['log_SFR_Ha'] # Target
from sklearn.model_selection import train_test_split
