import pandas as pd
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.ensemble import GradientBoostingRegressor, RandomForestRegressor
from sklearn.metrics import mean_squared_error, r2_score
import matplotlib.pyplot as plt

# --- 1. Load Datasets ---
compiled_sfr = pd.read_csv('compiled_sfr_dataset.csv')
magphys = pd.read_csv('MagPhys.csv')
stellar_masses = pd.read_csv('StellarMassesLambdar.csv')

# --- 2. Select Recommended Columns ---
# From MagPhys.csv
magphys_cols = ['CATAID', 'mass_stellar_best_fit', 'sSFR_0_1Gyr_best_fit', 'L_dust_best_fit', 
                'tau_V_best_fit', 'mass_dust_best_fit', 'metalicity_Z_Zo_percentile50', 'agem_percentile50']
magphys_selected = magphys[magphys_cols]

# From StellarMassesLambdar.csv
stellar_cols = ['CATAID', 'logmstar', 'extBV', 'gminusi', 'uminusr']
stellar_selected = stellar_masses[stellar_cols]

# --- 3. Merge Datasets ---
# Merge on 'CATAID' using a left join to keep all rows from compiled_sfr_data
merged_data = compiled_sfr.merge(magphys_selected, on='CATAID', how='left')
merged_data = merged_data.merge(stellar_selected, on='CATAID', how='left')

# --- 4. Define Target and Features ---
# Target column (assumed to be 'SFR' in compiled_sfr_data.csv; adjust if needed)
target_column = 'SFR'  # Change to 'sSFR_0_1Gyr_best_fit' if desired

# Feature columns
features = ['mass_stellar_best_fit', 'sSFR_0_1Gyr_best_fit', 'L_dust_best_fit', 
            'tau_V_best_fit', 'mass_dust_best_fit', 'metalicity_Z_Zo_percentile50', 
            'agem_percentile50', 'logmstar', 'extBV', 'gminusi', 'uminusr']

# --- 5. Clean Data ---
# Drop rows with missing values in target or features
data_clean = merged_data.dropna(subset=[target_column] + features)
print(f"Dataset size after cleaning: {data_clean.shape[0]} rows")

# Define X (features) and y (target)
X = data_clean[features]
y = data_clean[target_column]

# --- 6. Split Data ---
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# --- 7. Train Models ---
# Gradient Boosting Regressor
gb = GradientBoostingRegressor(random_state=42)
gb.fit(X_train, y_train)

# Random Forest Regressor
rf = RandomForestRegressor(random_state=42)
rf.fit(X_train, y_train)

# --- 8. Predict ---
y_pred_gb = gb.predict(X_test)
y_pred_rf = rf.predict(X_test)

# --- 9. Evaluate on Test Set ---
mse_gb = mean_squared_error(y_test, y_pred_gb)
r2_gb = r2_score(y_test, y_pred_gb)
mse_rf = mean_squared_error(y_test, y_pred_rf)
r2_rf = r2_score(y_test, y_pred_rf)

print(f"Gradient Boosting - MSE: {mse_gb:.4f}, R²: {r2_gb:.4f}")
print(f"Random Forest - MSE: {mse_rf:.4f}, R²: {r2_rf:.4f}")

# --- 10. Cross-Validation (5-fold) ---
cv_mse_gb = -cross_val_score(gb, X, y, cv=5, scoring='neg_mean_squared_error').mean()
cv_r2_gb = cross_val_score(gb, X, y, cv=5, scoring='r2').mean()
cv_mse_rf = -cross_val_score(rf, X, y, cv=5, scoring='neg_mean_squared_error').mean()
cv_r2_rf = cross_val_score(rf, X, y, cv=5, scoring='r2').mean()

# Corrected print statement (line 77)
print(f"CV MSE (GB): {cv_mse_gb:.4f}, CV R² (GB): {cv_r2_gb:.4f}")
print(f"CV MSE (RF): {cv_mse_rf:.4f}, CV R² (RF): {cv_r2_rf:.4f}")

# --- 11. Visualize Results ---
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