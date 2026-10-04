import pandas as pd
import numpy as np
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import PolynomialFeatures
from sklearn.metrics import mean_squared_error, r2_score
import matplotlib.pyplot as plt


# --- 1. Data Preparation ---
# Load the dataset
df = pd.read_csv('merged_data.csv')
print(f"Dataset loaded with {len(df)} rows and {len(df.columns)} columns.")


# Replace sentinel values (e.g., -9999) with NaN
df = df.replace(-9999, np.nan)


# Define target and features
target = 'log_SFR_Ha'
base_features = ['log_Mass_gas', 'nsa_mstar', 'log_Mass', 'V-band_SB_at_Re', 
                 'vel_sigma_Re', 'OH_Mar13_N2_Re_fit', 'Av_gas_Re']


# Impute missing values with median for robustness
imputer = SimpleImputer(strategy='median')
df[base_features] = imputer.fit_transform(df[base_features])


# Drop rows with missing target
df = df.dropna(subset=[target])
y = df[target]
X = df[base_features]


# --- 2. Feature Engineering ---
# Add interaction and nonlinear terms
df['log_Mass_gas_times_nsa_mstar'] = df['log_Mass_gas'] * df['nsa_mstar']
df['log_Mass_gas_times_metallicity'] = df['log_Mass_gas'] * df['OH_Mar13_N2_Re_fit']
df['log_Mass_gas_squared'] = df['log_Mass_gas'] ** 2


# Use PolynomialFeatures for systematic generation
poly = PolynomialFeatures(degree=2, include_bias=False)
X_poly = poly.fit_transform(X)
feature_names = poly.get_feature_names_out(base_features)


# --- 3. Model Training and Hyperparameter Tuning ---
# Split the data
X_train, X_test, y_train, y_test = train_test_split(X_poly, y, test_size=0.2, random_state=42)
print(f"Training set: {X_train.shape[0]} rows, Testing set: {X_test.shape[0]} rows")


# Define hyperparameter grid
param_grid = {
    'learning_rate': [0.01, 0.05, 0.1],
    'max_depth': [3, 5, 7],
    'n_estimators': [100, 200, 300]
}


# Initialize and tune Gradient Boosting model
gb = GradientBoostingRegressor(random_state=42)
grid_search = GridSearchCV(gb, param_grid, cv=5, scoring='neg_mean_squared_error', n_jobs=-1)
grid_search.fit(X_train, y_train)


# Get the best model
best_model = grid_search.best_estimator_
print(f"Best hyperparameters: {grid_search.best_params_}")


# --- 4. Model Evaluation ---
# Predict on test set
y_pred = best_model.predict(X_test)


# Calculate MSE and R-squared
mse = mean_squared_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)
print(f"Test MSE: {mse:.4f}")
print(f"Test R-squared: {r2:.4f}")


# Feature importance
importances = best_model.feature_importances_
importance_df = pd.DataFrame({'Feature': feature_names, 'Importance': importances})
print("\nTop 10 Important Features:")
print(importance_df.sort_values(by='Importance', ascending=False).head(10))


# Check residuals
residuals = y_test - y_pred
plt.figure(figsize=(8, 6))
plt.scatter(y_pred, residuals, alpha=0.5)
plt.axhline(0, color='red', linestyle='--')
plt.xlabel('Predicted log_SFR_Ha')
plt.ylabel('Residuals')
plt.title('Residuals vs. Predicted log_SFR_Ha')
plt.savefig('residuals.png')
plt.close()
print("Residual plot saved as 'residuals.png'. Inspect for patterns or biases.")


# --- 5. External Validation (Optional) ---
# Uncomment and adjust if you have an external dataset
