import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split, cross_val_score  # Added cross_val_score import
from sklearn.ensemble import GradientBoostingRegressor, RandomForestRegressor
from sklearn.metrics import mean_squared_error, r2_score
import matplotlib.pyplot as plt
import random

# Load dataset (make sure the path is correct)
sdss_data_path = 'SDSSDR18_200000.csv'  # Replace with correct path
df_main = pd.read_csv(sdss_data_path)

# Features to randomly select from
available_features = ['ra', 'dec', 'u', 'g', 'r', 'i', 'z', 'redshift']

# Randomly select 4 features (you can adjust this number as needed)
random_features = random.sample(available_features, 4)

# Target variable: 'redshift' (modify if you wish to target a different column)
target = 'redshift'

# Extract features (X) and target (y)
X = df_main[random_features]
y = df_main[target]

# Split data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Print out the selected features for reference
print(f"Selected random features: {random_features}")
print(f"Training set size: {X_train.shape[0]} rows")
print(f"Test set size: {X_test.shape[0]} rows")

# Training Gradient Boosting model
print("Training Gradient Boosting model...")
gb = GradientBoostingRegressor(random_state=42)
gb.fit(X_train, y_train)

# Training Random Forest model
print("Training Random Forest model...")
rf = RandomForestRegressor(random_state=42)
rf.fit(X_train, y_train)

# Evaluate the models
y_pred_gb = gb.predict(X_test)
y_pred_rf = rf.predict(X_test)

# Calculate MSE and R²
mse_gb = mean_squared_error(y_test, y_pred_gb)
r2_gb = r2_score(y_test, y_pred_gb)

mse_rf = mean_squared_error(y_test, y_pred_rf)
r2_rf = r2_score(y_test, y_pred_rf)

# Print model performance
print("\nModel Performance on Test Set:")
print(f"Gradient Boosting - MSE: {mse_gb:.4f}, R²: {r2_gb:.4f}")
print(f"Random Forest - MSE: {mse_rf:.4f}, R²: {r2_rf:.4f}")

# --- Perform 5-Fold Cross-Validation ---
print("\nPerforming 5-fold cross-validation...")
cv_mse_gb = -cross_val_score(gb, X, y, cv=5, scoring='neg_mean_squared_error').mean()
cv_r2_gb = cross_val_score(gb, X, y, cv=5, scoring='r2').mean()
cv_mse_rf = -cross_val_score(rf, X, y, cv=5, scoring='neg_mean_squared_error').mean()
cv_r2_rf = cross_val_score(rf, X, y, cv=5, scoring='r2').mean()

print(f"Cross-Validation MSE (Gradient Boosting): {cv_mse_gb:.4f}, R²: {cv_r2_gb:.4f}")
print(f"Cross-Validation MSE (Random Forest): {cv_mse_rf:.4f}, R²: {cv_r2_rf:.4f}")

# --- Visualize Results ---
# Plot Residuals for Gradient Boosting
plt.figure(figsize=(8, 6))
residuals_gb = y_test - y_pred_gb
plt.scatter(y_pred_gb, residuals_gb, alpha=0.5)
plt.axhline(0, color='red', linestyle='--')
plt.xlabel('Predicted Redshift (GB)')
plt.ylabel('Residuals')
plt.title('Residuals vs Predicted Redshift (Gradient Boosting)')
plt.savefig('residuals_gb.png')  # Save the figure instead of showing it

# Plot Residuals for Random Forest
plt.figure(figsize=(8, 6))
residuals_rf = y_test - y_pred_rf
plt.scatter(y_pred_rf, residuals_rf, alpha=0.5)
plt.axhline(0, color='red', linestyle='--')
plt.xlabel('Predicted Redshift (RF)')
plt.ylabel('Residuals')
plt.title('Residuals vs Predicted Redshift (Random Forest)')
plt.savefig('residuals_rf.png')  # Save the figure instead of showing it

# Feature Importance for Random Forest
plt.figure(figsize=(8, 6))
importances = rf.feature_importances_
sorted_idx = importances.argsort()
plt.barh(np.array(random_features)[sorted_idx], importances[sorted_idx])
plt.xlabel('Importance')
plt.title('Feature Importances (Random Forest)')
plt.savefig('feature_importance_rf.png')  # Save the figure instead of showing it

print("Plots have been saved as 'residuals_gb.png', 'residuals_rf.png', and 'feature_importance_rf.png'")
