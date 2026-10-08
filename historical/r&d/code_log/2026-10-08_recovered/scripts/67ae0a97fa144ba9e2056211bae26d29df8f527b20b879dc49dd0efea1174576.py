import pandas as pd
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.ensemble import GradientBoostingRegressor, RandomForestRegressor
from sklearn.metrics import mean_squared_error, r2_score
import matplotlib.pyplot as plt

# --- Load Datasets ---
magphys = pd.read_csv('MagPhys.csv')
stellar_masses = pd.read_csv('StellarMassesLambdar.csv')

# --- Merge Datasets on 'CATAID' ---
data = pd.merge(magphys, stellar_masses, on='CATAID', how='inner')

# --- Define Features and Target ---
# Features from MagPhys.csv and StellarMassesLambdar.csv
features = ['mass_stellar_best_fit', 'sSFR_0_1Gyr_best_fit', 'L_dust_best_fit', 
            'tau_V_best_fit', 'mass_dust_best_fit', 'metalicity_Z_Zo_percentile50', 
            'agem_percentile50', 'logmstar', 'extBV', 'gminusi', 'uminusr']

# Target: SFR from MagPhys.csv
target = 'SFR_0_1Gyr_best_fit'

# --- Clean Data ---
# Drop rows with missing values in target or features
data_clean = data.dropna(subset=[target] + features)
print(f"Dataset size after cleaning: {data_clean.shape[0]} rows")

# Define X (features) and y (target)
X = data_clean[features]
y = data_clean[target]

# --- Split Data ---
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# --- Train Models ---
# Gradient Boosting Regressor
gb = GradientBoostingRegressor(random_state=42)
gb.fit(X_train, y_train)

# Random Forest Regressor
rf = RandomForestRegressor(random_state=42)
rf.fit(X_train, y_train)

# --- Predict ---
y_pred_gb = gb.predict(X_test)
y_pred_rf = rf.predict(X_test)

# --- Evaluate on Test Set ---
mse_gb = mean_squared_error(y_test, y_pred_gb)
r2_gb = r2_score(y_test, y_pred_gb)
mse_rf = mean_squared_error(y_test, y_pred_rf)
r2_rf = r2_score(y_test, y_pred_rf)

print(f"Gradient Boosting - MSE: {mse_gb:.4f}, R²: {r2_gb:.4f}")
print(f"Random Forest - MSE: {mse_rf:.4f}, R²: {r2_rf:.4f}")

# --- Cross-Validation (5-fold) ---
cv_mse_gb = -cross_val_score(gb, X, y, cv=5, scoring='neg_mean_squared_error').mean()
cv_r2_gb = cross_val_score(gb, X, y, cv=5, scoring='r2').mean()
cv_mse_rf = -cross_val_score(rf, X, y, cv=5, scoring='neg_mean_squared_error').mean()
cv_r2_rf = cross_val_score(rf, X, y, cv=5, scoring='r2').mean()

print(f"CV MSE (GB): {cv_mse_gb:.4f}, CV R² (GB): {cv_r2_gb:.4f}")
print(f"CV MSE (RF): {cv_mse_rf:.4f}, CV R² (RF): {cv_r2_rf:.4f}")

# --- Visualize Results ---
# Residual plot for Random Forest
plt.figure(figsize=(8, 6))
residuals_rf = y_test - y_pred_rf
plt.scatter(y_pred_rf, residuals_rf, alpha=0.5)
plt.axhline(0, color='red', linestyle='--')
plt.xlabel('Predicted SFR')
plt.ylabel('Residuals')
plt.title('Residuals vs. Predicted (Random Forest)')
plt.show()

# Feature importance for Random Forest
plt.figure(figsize=(8, 6))
importances = rf.feature_importances_
feature_names = X.columns
sorted_idx = importances.argsort()
plt.barh(feature_names[sorted_idx], importances[sorted_idx])
plt.xlabel('Importance')
plt.title('Feature Importances (Random Forest)')
plt.show()