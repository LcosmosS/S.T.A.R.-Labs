import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.preprocessing import PolynomialFeatures
from sklearn.impute import SimpleImputer
import matplotlib.pyplot as plt
import io

# --- Embedded Datasets ---
# You would replace these with your actual data loading
# For demonstration, let's create some dummy dataframes:
magphys_data = """
CATAID,mass_stellar_best_fit,sSFR_0_1Gyr_best_fit,L_dust_best_fit,tau_V_best_fit,mass_dust_best_fit,metalicity_Z_Zo_percentile50,agem_percentile50,SFR_0_1Gyr_best_fit
1,1e10,-11,1e4,1,1e6,0.5,5,1
2,5e9,-10.5,5e3,0.8,5e5,0.6,6,0.5
3,2e10,-10,2e4,1.2,2e6,0.7,7,2
4,8e9,-11.5,8e3,0.6,8e5,0.55,5.5,0.8
5,1.5e10,-9.5,1.5e4,1.1,1.5e6,0.65,6.5,1.5
"""
stellar_masses_data = """
CATAID,logmstar,extBV,gminusi,uminusr
1,10,0.1,0.5,1.5
2,9.7,0.15,0.6,1.6
3,10.3,0.08,0.4,1.4
4,9.9,0.12,0.55,1.55
5,10.2,0.11,0.45,1.45
"""
galaxies_classified_data = """
CATAID,Z,GeoS4,GeoS10
1,0.1,0.8,0.9
2,0.08,0.75,0.85
3,0.12,0.85,0.95
4,0.09,0.78,0.88
5,0.11,0.82,0.92
"""
environment_measures_data = """
CATAID,DistanceTo5nn,SurfaceDensity,CountInCyl,AGEDenPar
1,10,5,15,2
2,12,6,18,2.5
3,8,4,12,1.5
4,11,5.5,16.5,2.2
5,9,4.5,13.5,1.8
"""

df = pd.DataFrame({
    'log_Mass_gas': [10.5, 9.8, 11.2, 10.1, 9.9, 10.7, 11.5, 9.6, 10.3, 10.9],
    'nsa_mstar': [11.1, 10.5, 11.8, 10.9, 10.7, 11.3, 12.0, 10.2, 10.8, 11.4],
    'OH_Mar13_N2_Re_fit': [8.5, -9999, 8.7, 8.6, -9999, 8.8, 8.9, 8.4, 8.6, -9999],
    'Av_gas_Re': [1.2, 1.5, -9999, 1.3, 1.4, 1.6, 1.1, -9999, 1.3, 1.7],
    'log_Mass': [10.8, 10.2, 11.5, 10.4, 10.3, 10.9, 11.7, 10.0, 10.6, 11.2],
    'V-band_SB_at_Re': [22.5, 23.0, 21.8, 22.3, 22.7, 22.0, 21.5, 23.2, 22.6, 21.9],
    'vel_sigma_Re': [150, 120, 180, 130, 140, 160, 200, 110, 135, 170],
    'log_SFR_Ha': [0.8, 0.5, 1.2, 0.7, 0.6, 1.0, 1.5, 0.4, 0.9, 1.1],
    'QCFLAG': [1, 1, 0, 1, 0, 1, 1, 0, 1, 1]
})

# --- Load DataFrames ---
magphys = pd.read_csv(io.StringIO(magphys_data))
stellar_masses = pd.read_csv(io.StringIO(stellar_masses_data))
galaxies_classified = pd.read_csv(io.StringIO(galaxies_classified_data))
environment_measures = pd.read_csv(io.StringIO(environment_measures_data))

# --- Merge DataFrames ---
data = pd.merge(magphys, stellar_masses, on='CATAID', how='inner')
data = pd.merge(data, galaxies_classified, on='CATAID', how='inner')
data = pd.merge(data, environment_measures, on='CATAID', how='inner')

# --- Merge into main DataFrame ---
df = pd.merge(df, data, how='left', left_index=True, right_index=True)

# --- Clean Data: Handle Missing Values ---
df[['OH_Mar13_N2_Re_fit', 'Av_gas_Re']] = df[['OH_Mar13_N2_Re_fit', 'Av_gas_Re']].replace(-9999, np.nan)
imputer = SimpleImputer(strategy='median')
df[['OH_Mar13_N2_Re_fit', 'Av_gas_Re']] = imputer.fit_transform(df[['OH_Mar13_N2_Re_fit', 'Av_gas_Re']])

# --- Quality Control ---
df = df[df['QCFLAG'] == 1]

# --- Feature Engineering: Interaction and Nonlinear Terms ---
poly = PolynomialFeatures(degree=2, interaction_only=False, include_bias=False)
features = ['log_Mass_gas', 'nsa_mstar', 'OH_Mar13_N2_Re_fit', 'Av_gas_Re', 'log_Mass', 'V-band_SB_at_Re', 'vel_sigma_Re']
X = df[features]
X_poly = poly.fit_transform(X)
feature_names = poly.get_feature_names_out(features)
df_poly = pd.DataFrame(X_poly, columns=feature_names)

# --- Split Data ---
X_train, X_test, y_train, y_test = train_test_split(df_poly, df['log_SFR_Ha'], test_size=0.2, random_state=42)

# --- Random Forest Model with GridSearchCV ---
print("Tuning Random Forest model...")
param_grid_rf = {'n_estimators': [100, 200, 300], 'max_depth': [10, 20, None], 'min_samples_split': [2, 5, 10]}
rf_model = RandomForestRegressor(random_state=42)
grid_search_rf = GridSearchCV(estimator=rf_model, param_grid=param_grid_rf, cv=5, scoring='neg_mean_squared_error', n_jobs=-1)
grid_search_rf.fit(X_train, y_train)
best_rf_model = grid_search_rf.best_estimator_

# --- Gradient Boosting Model with GridSearchCV ---
print("Tuning Gradient Boosting model...")
param_grid_gb = {'learning_rate': [0.01, 0.05, 0.1], 'max_depth': [3, 5, 7], 'n_estimators': [100, 200, 300]}
gb_model = GradientBoostingRegressor(random_state=42)
grid_search_gb = GridSearchCV(estimator=gb_model, param_grid=param_grid_gb, cv=5, scoring='neg_mean_squared_error', n_jobs=-1)
grid_search_gb.fit(X_train, y_train)
best_gb_model = grid_search_gb.best_estimator_

# --- Make Predictions ---
y_pred_rf = best_rf_model.predict(X_test)
y_pred_gb = best_gb_model.predict(X_test)

# --- Evaluate Models ---
mse_rf = mean_squared_error(y_test, y_pred_rf)
r2_rf = r2_score(y_test, y_pred_rf)
mse_gb = mean_squared_error(y_test, y_pred_gb)
r2_gb = r2_score(y_test, y_pred_gb)

print("\nModel Performance:")
print(f"Random Forest - MSE: {mse_rf:.4f}, R²: {r2_rf:.4f}")
print(f"Gradient Boosting - MSE: {mse_gb:.4f}, R²: {r2_gb:.4f}")

# --- Feature Importances (Random Forest) ---
importances_rf = best_rf_model.feature_importances_
feature_importances_rf = pd.Series(importances_rf, index=feature_names)
feature_importances_rf_sorted = feature_importances_rf.sort_values(ascending=False)

print("\nRandom Forest Feature Importances:")
print(feature_importances_rf_sorted)

# --- Feature Importances (Gradient Boosting) ---
importances_gb = best_gb_model.feature_importances_
feature_importances_gb = pd.Series(importances_gb, index=feature_names)
feature_importances_gb_sorted = feature_importances_gb.sort_values(ascending=False)

print("\nGradient Boosting Feature Importances:")
print(feature_importances_gb_sorted)

# --- Visualize Results ---
# Residual Plot for Random Forest
plt.figure(figsize=(10, 6))
residuals_rf = y_test - y_pred_rf
plt.scatter(y_pred_rf, residuals_rf, alpha=0.5)
plt.axhline(0, color='red', linestyle='--')
plt.xlabel('Predicted log_SFR_Ha')
plt.ylabel('Residuals')
plt.title('Residuals vs Predicted SFR (Random Forest)')
plt.show()

# Feature Importance Plot (Random Forest)
plt.figure(figsize=(12, 8))
feature_importances_rf_sorted.plot(kind='barh')
plt.xlabel('Importance')
plt.title('Random Forest Feature Importances')
plt.show()

# --- Print Best Parameters ---
print("\nBest parameters found by Random Forest's grid search:")
print(grid_search_rf.best_params_)

print("\nBest parameters found by Gradient Boosting's grid search:")
print(grid_search_gb.best_params_)

# --- Printing BSD values
def calculate_k(masses):
    """Calculates the normalization constant K."""
    m0 = np.median(masses)
    sum_mi_m0 = np.sum(masses / m0)
    sum_m0_mi = np.sum(m0 / masses)
    return sum_mi_m0 / sum_m0_mi

def cosmological_l_function(data, s):
    """Computes the cosmological L-function."""
    logmass_values = data['log_Mass_gas'].values  # Using 'logmass' as logmass
    l_value = np.sum((logmass_values / np.median(logmass_values))**(-s))
    return l_value

L_1 = cosmological_l_function(df, 1)

print(f"L-function at s=1: {L_1:.4f}")

# Save the model (optional)
joblib.dump(best_rf_model, 'best_rf_model.joblib')
