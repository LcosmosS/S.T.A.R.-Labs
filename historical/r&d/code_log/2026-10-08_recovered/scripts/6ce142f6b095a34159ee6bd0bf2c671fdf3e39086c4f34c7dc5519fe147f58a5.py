import pandas as pd
import numpy as np
from sklearn.ensemble import GradientBoostingRegressor, RandomForestRegressor
from sklearn.model_selection import train_test_split, RandomizedSearchCV
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt

# --- 1. Load the Dataset ---
print("Loading SDSSDR18_G.csv...")
df = pd.read_csv('SDSSDR18_G.csv')
print(f"Dataset shape: {df.shape}")

# --- 2. Preprocess the Data ---
# Check for missing values and drop rows with any
print("Checking for missing values...")
print(df.isnull().sum())
df = df.dropna()
print(f"Rows after dropping missing values: {df.shape[0]}")

# Define features and target
features = ['spec_z', 'zErr', 'stellar_mass', 'g_r_color']
X = df[features]
y = df['sfr']

# --- 3. Split the Data ---
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
print(f"Training samples: {X_train.shape[0]}, Test samples: {X_test.shape[0]}")

# --- 4. Scale the Features ---
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# --- 5. Define Hyperparameter Grids ---
rf_params = {
    'n_estimators': [100, 200, 300],
    'max_depth': [10, 20, None],
    'min_samples_split': [2, 5, 10]
}

gb_params = {
    'learning_rate': [0.01, 0.05, 0.1],
    'max_depth': [3, 5, 7],
    'n_estimators': [100, 200, 300]
}

# --- 6. Train Random Forest with Tuning ---
print("Tuning Random Forest...")
rf = RandomForestRegressor(random_state=42)
rf_random = RandomizedSearchCV(rf, rf_params, n_iter=10, cv=3, scoring='neg_mean_squared_error', 
                              n_jobs=-1, random_state=42)
rf_random.fit(X_train_scaled, y_train)
best_rf = rf_random.best_estimator_
print(f"Best RF parameters: {rf_random.best_params_}")

# --- 7. Train Gradient Boosting with Tuning ---
print("Tuning Gradient Boosting...")
gb = GradientBoostingRegressor(random_state=42)
gb_random = RandomizedSearchCV(gb, gb_params, n_iter=10, cv=3, scoring='neg_mean_squared_error', 
                              n_jobs=-1, random_state=42)
gb_random.fit(X_train_scaled, y_train)
best_gb = gb_random.best_estimator_
print(f"Best GB parameters: {gb_random.best_params_}")

# --- 8. Make Predictions ---
rf_pred = best_rf.predict(X_test_scaled)
gb_pred = best_gb.predict(X_test_scaled)
gbrf_pred = (rf_pred + gb_pred) / 2  # Average predictions for GBRF

# --- 9. Evaluate the Model ---
mse = mean_squared_error(y_test, gbrf_pred)
r2 = r2_score(y_test, gbrf_pred)
print("\nGBRF Model Performance:")
print(f"Mean Squared Error (MSE): {mse:.4f}")
print(f"R-squared (R²): {r2:.4f}")

# --- 10. Generate and Save Residual Plot ---
residuals = y_test - gbrf_pred
plt.figure(figsize=(8, 6))
plt.scatter(gbrf_pred, residuals, alpha=0.5)
plt.axhline(0, color='red', linestyle='--')
plt.xlabel('Predicted SFR')
plt.ylabel('Residuals')
plt.title('Residuals vs Predicted SFR (GBRF)')
plt.savefig('gbrf_residuals.png')
plt.close()
print("Residual plot saved as 'gbrf_residuals.png'.")