import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
import numpy as np
# ... (other imports)


# Load data
df = pd.read_csv('compiled_sfr_dataset.csv')
print(f"Dataset loaded with {df.shape[0]} rows and {df.shape[1]} columns.")
target = 'your_target_column'  # Replace with your target column name
y = df[target]
X = df.drop(columns=[target])
# ... (preprocessing, e.g., creating X_poly)


# Identify outliers
Q1, Q3 = y.quantile(0.25), y.quantile(0.75)
IQR = Q3 - Q1
outliers = (y < Q1 - 1.5 * IQR) | (y > Q3 + 1.5 * IQR)
print(f"Number of outliers in target: {outliers.sum()}")


# Split data
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
print(f"Training set: {X_train.shape[0]} rows, Testing set: {X_test.shape[0]} rows")


# ... (model training, hyperparameter tuning)


# Evaluate models
rf_results = evaluate_model(best_rf, X_test, y_test, outliers, ~outliers)
gb_results = evaluate_model(best_gb, X_test, y_test, outliers, ~outliers)
