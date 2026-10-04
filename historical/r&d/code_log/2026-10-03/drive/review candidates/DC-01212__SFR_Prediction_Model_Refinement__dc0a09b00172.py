import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.ensemble import GradientBoostingRegressor, RandomForestRegressor
from sklearn.metrics import mean_squared_error, r2_score


# Load StellarMassesLambdar.csv dataset
stellar_data_path = 'StellarMassesLambdar.csv'  # Correct path to your StellarMassesLambdar file
df_stellar = pd.read_csv(stellar_data_path)


# List of all available columns in the dataset
columns = df_stellar.columns.tolist()


# Randomly select a subset of features (let's say 6 features)
random_features = np.random.choice(columns, size=6, replace=False)


# Select target variable (you can modify this as needed, using 'logmstar' as an example target)
target = 'logmstar'


# Extract features (X) and target (y)
X = df_stellar[random_features]
y = df_stellar[target]


# Split data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)


# Train Gradient Boosting model
print("Training Gradient Boosting model...")
gb = GradientBoostingRegressor(random_state=42)
gb.fit(X_train, y_train)


# Train Random Forest model
print("Training Random Forest model...")
rf = RandomForestRegressor(random_state=42)
rf.fit(X_train, y_train)


# Evaluate the models
y_pred_gb = gb.predict(X_test)
y_pred_rf = rf.predict(X_test)


# Calculate MSE and R^2
mse_gb = mean_squared_error(y_test, y_pred_gb)
r2_gb = r2_score(y_test, y_pred_gb)


mse_rf = mean_squared_error(y_test, y_pred_rf)
r2_rf = r2_score(y_test, y_pred_rf)


# Print model performance
print("\nModel Performance on Test Set:")
print(f"Gradient Boosting - MSE: {mse_gb:.4f}, R²: {r2_gb:.4f}")
print(f"Random Forest - MSE: {mse_rf:.4f}, R²: {r2_rf:.4f}")


# Perform 5-fold cross-validation
cv_mse_gb = -cross_val_score(gb, X, y, cv=5, scoring='neg_mean_squared_error').mean()
cv_r2_gb = cross_val_score(gb, X, y, cv=5, scoring='r2').mean()


cv_mse_rf = -cross_val_score(rf, X, y, cv=5, scoring='neg_mean_squared_error').mean()
cv_r2_rf = cross_val_score(rf, X, y, cv=5, scoring='r2').mean()


# Print cross-validation results
print(f"\nCross-Validation MSE (Gradient Boosting): {cv_mse_gb:.4f}, R²: {cv_r2_gb:.4f}")
print(f"Cross-Validation MSE (Random Forest): {cv_mse_rf:.4f}, R²: {cv_r2_rf:.4f}")
