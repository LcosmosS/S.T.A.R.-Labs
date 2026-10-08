import pandas as pd
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.ensemble import GradientBoostingRegressor, RandomForestRegressor
from sklearn.metrics import mean_squared_error, r2_score
import matplotlib.pyplot as plt

# --- Load Datasets ---
print("Loading datasets...")
magphys = pd.read_csv('MagPhys.csv')[['CATAID', 'mass_stellar_best_fit', 'sSFR_0_1Gyr_best_fit',
                                      'L_dust_best_fit', 'tau_V_best_fit', 'mass_dust_best_fit',
                                      'metalicity_Z_Zo_percentile50', 'agem_percentile50',
                                      'SFR_0_1Gyr_best_fit']]
stellar_masses = pd.read_csv('StellarMassesLambdar.csv')[['CATAID', 'logmstar', 'extBV', 'gminusi', 'uminusr']]
galaxies_classified = pd.read_csv('GalaxiesClassified.csv')[['CATAID', 'Z', 'GeoS4', 'GeoS10']]
environment_measures = pd.read_csv('EnvironmentMeasures.csv')[['CATAID', 'DistanceTo5nn', 'SurfaceDensity',
                                                               'CountInCyl', 'AGEDenPar']]

# --- Merge Datasets ---
print("Merging datasets on 'CATAID'...")
data = pd.merge(magphys, stellar_masses, on='CATAID', how='inner')
data = pd.merge(data, galaxies_classified, on='CATAID', how='inner')
data = pd.merge(data, environment_measures, on='CATAID', how='inner')

# --- Clean Data ---
print("Cleaning data...")
features_prelim = [
    'mass_stellar_best_fit', 'sSFR_0_1Gyr_best_fit', 'L_dust_best_fit',
    'tau_V_best_fit', 'mass_dust_best_fit', 'metalicity_Z_Zo_percentile50',
    'agem_percentile50', 'logmstar', 'extBV', 'gminusi', 'uminusr',
    'Z', 'GeoS4', 'GeoS10', 'DistanceTo5nn', 'SurfaceDensity',
    'CountInCyl', 'AGEDenPar'
]
target = 'SFR_0_1Gyr_best_fit'
data_clean = data.dropna(subset=[target] + features_prelim)
print(f"Dataset size after cleaning: {data_clean.shape[0]} rows")

# --- Feature Engineering ---
print("Creating engineered features...")
data_clean['mass_to_dust'] = data_clean['mass_stellar_best_fit'] / data_clean['mass_dust_best_fit']
data_clean['color_gradient'] = data_clean['uminusr'] - data_clean['gminusi']
data_clean['atten_metal'] = data_clean['tau_V_best_fit'] * data_clean['metalicity_Z_Zo_percentile50']

# --- Final Feature List ---
features = features_prelim + ['mass_to_dust', 'color_gradient', 'atten_metal']

# --- Train/Test Split ---
X = data_clean[features]
y = data_clean[target]
print("Splitting data...")
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# --- Train Models ---
print("Training Gradient Boosting...")
gb = GradientBoostingRegressor(random_state=42)
gb.fit(X_train, y_train)

print("Training Random Forest...")
rf = RandomForestRegressor(random_state=42)
rf.fit(X_train, y_train)

# --- Predictions & Evaluation ---
y_pred_gb = gb.predict(X_test)
y_pred_rf = rf.predict(X_test)

mse_gb = mean_squared_error(y_test, y_pred_gb)
r2_gb = r2_score(y_test, y_pred_gb)
mse_rf = mean_squared_error(y_test, y_pred_rf)
r2_rf = r2_score(y_test, y_pred_rf)

print("\nModel Performance on Test Set:")
print(f"Gradient Boosting - MSE: {mse_gb:.4f}, R²: {r2_gb:.4f}")
print(f"Random Forest     - MSE: {mse_rf:.4f}, R²: {r2_rf:.4f}")

# --- 5-Fold Cross-Validation ---
print("\nPerforming 5-fold cross-validation...")
cv_mse_gb = -cross_val_score(gb, X, y, cv=5, scoring='neg_mean_squared_error').mean()
cv_r2_gb = cross_val_score(gb, X, y, cv=5, scoring='r2').mean()
cv_mse_rf = -cross_val_score(rf, X, y, cv=5, scoring='neg_mean_squared_error').mean()
cv_r2_rf = cross_val_score(rf, X, y, cv=5, scoring='r2').mean()

print(f"Cross-Validation (GB) - MSE: {cv_mse_gb:.4f}, R²: {cv_r2_gb:.4f}")
print(f"Cross-Validation (RF) - MSE: {cv_mse_rf:.4f}, R²: {cv_r2_rf:.4f}")

# --- Visualizations ---
# Residual Plot - RF
plt.figure(figsize=(8, 6))
residuals_rf = y_test - y_pred_rf
plt.scatter(y_pred_rf, residuals_rf, alpha=0.5)
plt.axhline(0, color='red', linestyle='--')
plt.xlabel('Predicted SFR')
plt.ylabel('Residuals')
plt.title('Residuals vs Predicted SFR (Random Forest)')
plt.show()

# Feature Importance - RF
plt.figure(figsize=(9, 6))
importances = rf.feature_importances_
sorted_idx = importances.argsort()
plt.barh(X.columns[sorted_idx], importances[sorted_idx])
plt.xlabel('Importance')
plt.title('Feature Importances (Random Forest)')
plt.tight_layout()
plt.show()
