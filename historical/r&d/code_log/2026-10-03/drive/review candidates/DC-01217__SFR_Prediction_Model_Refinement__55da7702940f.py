import pandas as pd
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.ensemble import GradientBoostingRegressor, RandomForestRegressor
from sklearn.metrics import mean_squared_error, r2_score
import matplotlib.pyplot as plt
import random


# --- Load Dataset --- 
print("Loading dataset...")
df = pd.read_csv('SDSSDR18_200000.csv')  # Replace with correct path


# --- Columns to target ---
features = ['ra', 'dec', 'r', 'z', 'i', 'fiberid', 'log_Mass', 'metallicity']  # Target features
target = 'SFR'  # Targeting Star Formation Rate for prediction


# --- Clean Data ---
print("Cleaning data...")
df_clean = df[features + [target]].dropna()
print(f"Dataset size after cleaning: {df_clean.shape[0]} rows")


# --- Split Data into Training and Testing Sets ---
print("Splitting data into training and testing sets...")
X = df_clean[features]
y = df_clean[target]


X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)


print(f"Training set size: {X_train.shape[0]} rows")
print(f"Test set size: {X_test.shape[0]} rows")


# --- Train Models ---
print("Training Gradient Boosting model...")
gb = GradientBoostingRegressor(random_state=42)
gb.fit(X_train, y_train)


print("Training Random Forest model...")
rf = RandomForestRegressor(random_state=42)
rf.fit(X_train, y_train)


# --- Make Predictions ---
y_pred_gb = gb.predict(X_test)
y_pred_rf = rf.predict(X_test)


# --- Evaluate Models on Test Set ---
mse_gb = mean_squared_error(y_test, y_pred_gb)
r2_gb = r2_score(y_test, y_pred_gb)


mse_rf = mean_squared_error(y_test, y_pred_rf)
r2_rf = r2_score(y_test, y_pred_rf)


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
plt.xlabel('Predicted SFR (GB)')
plt.ylabel('Residuals')
plt.title('Residuals vs Predicted SFR (Gradient Boosting)')
plt.savefig('residuals_gb.png')


# Plot Residuals for Random Forest
plt.figure(figsize=(8, 6))
residuals_rf = y_test - y_pred_rf
plt.scatter(y_pred_rf, residuals_rf, alpha=0.5)
plt.axhline(0, color='red', linestyle='--')
plt.xlabel('Predicted SFR (RF)')
plt.ylabel('Residuals')
plt.title('Residuals vs Predicted SFR (Random Forest)')
plt.savefig('residuals_rf.png')


# Feature Importance for Random Forest
plt.figure(figsize=(8, 6))
importances = rf.feature_importances_
sorted_idx = importances.argsort()
plt.barh(np.array(features)[sorted_idx], importances[sorted_idx])
plt.xlabel('Importance')
plt.title('Feature Importances (Random Forest)')
plt.savefig('feature_importance_rf.png')


print("Plots have been saved as 'residuals_gb.png', 'residuals_rf.png', and 'feature_importance_rf.png'")
