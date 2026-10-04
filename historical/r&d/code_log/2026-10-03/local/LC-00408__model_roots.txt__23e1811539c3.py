import pandas as pd
from sklearn.model_selection import train_test_split


# Load the filtered dataset
df = pd.read_csv('Filtered_Pipe3D.csv')
print(f"Dataset loaded with {len(df)} rows and {len(df.columns)} columns.")


# Define the target variable and features
X = df.drop(columns=['log_SFR_Ha'])  # Features (all columns except the target)
y = df['log_SFR_Ha']                 # Target (log_SFR_Ha)


# Split the data into training and testing sets (80% train, 20% test)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)


# Print the sizes of the training and testing sets
print(f"Training set: {X_train.shape[0]} rows, {X_train.shape[1]} columns")
print(f"Testing set: {X_test.shape[0]} rows, {X_test.shape[1]} columns")
