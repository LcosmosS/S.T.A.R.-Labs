import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.preprocessing import PolynomialFeatures, StandardScaler
from sklearn.impute import SimpleImputer
import matplotlib.pyplot as plt

# --- Filepaths ---
magphys_filepath = 'MagPhys.csv'
stellar_masses_filepath = 'StellarMassesLambdar.csv'
galaxies_classified_filepath = 'GalaxiesClassified.csv'
environment_measures_filepath = 'EnvironmentMeasures.csv'
main_df_filepath = 'MainDataFrame.csv'

# --- Load Datasets ---
print("Loading datasets...")
magphys = pd.read_csv(magphys_filepath)[['CATAID', 'mass_stellar_best_fit', 'sSFR_0_1Gyr_best_fit', 
                                      'L_dust_best_fit', 'tau_V_best_fit', 'mass_dust_best_fit', 
                                      'metalicity_Z_Zo_percentile50', 'agem_percentile50', 
                                      'SFR_0_1Gyr_best_fit']]
stellar_masses = pd.read_csv(stellar_masses_filepath)[['CATAID', 'logmstar', 'extBV', 'gminusi', 'uminusr']]
galaxies_classified = pd.read_csv(galaxies_classified_filepath)[['CATAID', 'Z', 'GeoS4', 'GeoS10']]
environment_measures = pd.read_csv(environment_measures_filepath)[['CATAID', 'DistanceTo5nn', 'SurfaceDensity', 
                                                               'CountInCyl', 'AGEDenPar']]

# --- Load main DataFrame ---
df = pd.read_csv(main_df_filepath)

# --- Merge DataFrames ---
print("Merging datasets...")
data = pd.merge(magphys, stellar_masses, on='CATAID', how='inner')
data = pd.merge(data, galaxies_classified, on='CATAID', how='inner')
data = pd.merge(data, environment_measures, on='CATAID', how='inner')

# --- Merge into main DataFrame ---
df = pd.merge(df, data, how='left', left_index=True, right_index=True)

# --- Clean Data: Handle Missing Values ---
print("Handling missing values...")
df[['OH_Mar13_N2_Re_fit', 'Av_gas_Re']] = df[['OH_Mar13_N2_Re_fit', 'Av_gas_Re']].replace(-9999, np.nan)
imputer = SimpleImputer(strategy='median')
df[['OH_Mar13_N2_Re_fit', 'Av_gas_Re']] = imputer.fit_transform(df[['OH_Mar13_N2_Re_fit', 'Av_gas_Re']])

# --- Quality Control ---
print("Applying quality control...")
df = df[df['QCFLAG'] == 1]

# --- Feature Engineering: Interaction and Nonlinear Terms ---
print("Engineering features...")
poly = PolynomialFeatures(degree=2, interaction_only=False, include_bias=False)
features = ['log_Mass_gas', 'nsa_mstar', 'OH_Mar13_N2_Re_fit', 'Av_gas_Re', 'log_Mass', 'V-band_SB_at_Re', 'vel_sigma_Re']
X = df[features]
X_poly = poly.fit_transform(X)
feature_names = poly.get_feature_names_out(features)
df_poly = pd.DataFrame(X_poly, columns=feature_names)

# --- BSD Conjecture Implementation ---
def calculate_k(masses):
    """Calculates the normalization constant K."""
    m0 = np.median(masses)
    sum_mi_m0 = np.sum(masses / m0)
    sum_m0_mi = np.sum(m0 / masses)
    return sum_mi_m0 / sum_m0_mi

def cosmological_l_function(data, s):
    """Computes the cosmological L-function."""
    logmass_values = data['log_Mass_gas'].values  # Using log_Mass_gas from DataFrame
    l_value = np.sum((logmass_values / np.median(logmass_values))**(-s))
    return l_value

# --- Calculate L-function ---
L_1 = cosmological_l_function(df, 1)
print(f"L-function at s=1: {L_1:.4f}")

# --- Split Data ---
print("Splitting data...")
X_train, X_test, y_train, y_test = train_test_split(df_poly, df['log_SFR_Ha'], test_size=0.2, random_state=42)

# --- Standardize features ---
print("Standardizing features...")
scaler = StandardScaler()
X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)

# --- Random Forest Model with GridSearchCV ---
print("Tuning Random Forest model...")
param_grid_rf = {'n_estimators': [200, 300], 'max_depth': [10, None], 'min_samples_split': [2, 5]} # Reduced search space
rf_model = RandomForestRegressor(random_state=42)
grid_search_rf = GridSearchCV(estimator=rf_model, param_grid=param_grid_rf, scoring='neg_mean_squared_error', cv=3, n_jobs=-1)
grid_search_rf.fit(X_train, y_train)
best_rf_model = grid_search_rf.best_estimator_

# --- Gradient Boosting Model with GridSearchCV ---
print("Tuning Gradient Boosting model...")
param_grid_gb = {'learning_rate': [0.01, 0.05], 'max_depth': [3, 5], 'n_estimators': [200, 300]} # Reduced search space
gb_model = GradientBoostingRegressor(random_state=42)
grid_search_gb = GridSearchCV(estimator=gb_model, param_grid=param_grid_gb, scoring='neg_mean_squared_error', cv=3, n_jobs=-1)
grid_search_gb.fit(X_train, y_train)
best_gb_model = grid_search_gb.best_estimator_

# --- Make Predictions ---
print("Making predictions...")
y_pred_rf = best_rf_model.predict(X_test)
y_pred_gb = best_gb_model.predict(X_test)

# --- Evaluate Models ---
print("Evaluating models...")
mse_rf = mean_squared_error(y_test, y_pred_rf)
r2_rf = r2_score(y_test, y_pred_rf)
mse_gb = mean_squared_error(y_test, y_pred_gb)
r2_gb = r2_score(y_test, y_pred_gb)

print("\nModel Performance:")
print(f"Random Forest - MSE: {mse_rf:.4f}, R²: {r2_rf:.4f}")
print(f"Gradient Boosting - MSE: {mse_gb:.4f}, R²: {r2_gb:.4f}")

# --- Feature Importances (Random Forest) ---
print("Analyzing feature importances...")
importances_rf = best_rf_model.feature_importances_
feature_importances_rf = pd.Series(importances_rf, index=feature_names)
feature_importances_rf_sorted = feature_importances_rf.sort_values(ascending=False)

print("\nRandom Forest Feature Importances:")
print(feature_importances_rf_sorted)

# --- BSD check (correctly use feature names)
def BSD_conjecture(model, importances, feature_names):
    """Checks the BSD conjecture based on feature importances."""
    
    # Create a dictionary to map feature names to their importances
    importance_dict = dict(zip(feature_names, importances))
    
    # Function to safely get importance from the dictionary
    def get_importance(feature):
        return importance_dict.get(feature, 0)  # Return 0 if feature not found

    log_Mass_gas_importance = get_importance('log_Mass_gas')
    nsa_mstar_importance = get_importance('nsa_mstar')
    times_log_Mass_importance = get_importance('log_Mass_gas nsa_mstar')  # Correct interaction term
    
    if (log_Mass_gas_importance > 0.8 and nsa_mstar_importance < 0.15 and times_log_Mass_importance < 0.12):
        print("The BSD conjecture seems to hold based on these feature importances.")
    else:
        print("The BSD conjecture does not seem to hold based on these feature importances.")

# Test with new BSD_conjecture function call
BSD_conjecture(best_rf_model, feature_importances_rf, feature_names)

# --- Visualize Results ---
# Residual Plot for Random Forest
plt.figure(figsize=(8, 6))
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
    logmass_values = data['log_Mass_gas'].values  # Using logmass' as logmass
    l_value = np.sum((logmass_values / np.median(logmass_values))**(-s))
    return l_value
