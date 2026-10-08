import pandas as pd
import numpy as np
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

# --- Merge Datasets on 'CATAID' ---
print("Merging datasets on 'CATAID'...")
data = pd.merge(magphys, stellar_masses, on='CATAID', how='inner')
data = pd.merge(data, galaxies_classified, on='CATAID', how='inner')
data = pd.merge(data, environment_measures, on='CATAID', how='inner')

# --- Define Relevant Features and Target ---
features = [
    # From MagPhys.csv
    'mass_stellar_best_fit',       # Stellar mass best fit
    'sSFR_0_1Gyr_best_fit',        # Specific SFR over the last 0.1 Gyr
    'L_dust_best_fit',             # Dust luminosity
    'tau_V_best_fit',              # Optical depth
    'mass_dust_best_fit',          # Dust mass
    'metalicity_Z_Zo_percentile50',# Metallicity (50th percentile)
    'agem_percentile50',           # Stellar age (50th percentile)
    # From StellarMassesLambdar.csv
    'logmstar',                    # Log stellar mass
    'extBV',                       # Extinction in B-V
    'gminusi',                     # g-i color index
    'uminusr',                     # u-r color index
    # From GalaxiesClassified.csv
    'Z',                           # Redshift
    'GeoS4',                       # Geometric parameter S4
    'GeoS10',                      # Geometric parameter S10
    # From EnvironmentMeasures.csv
    'DistanceTo5nn',               # Distance to 5th nearest neighbor
    'SurfaceDensity',              # Surface density
    'CountInCyl',                  # Count in cylinder
    'AGEDenPar'                    # Age density parameter
]

# Target variable: SFR over the last 0.1 Gyr from MagPhys
target = 'SFR_0_1Gyr_best_fit'

# --- Clean Data ---
print("Cleaning data...")
data_clean = data.dropna(subset=[target] + features)
print(f"Dataset size after cleaning: {data_clean.shape[0]} rows")

# Extract features (X) and target (y)
X = data_clean[features].copy()  # Create a copy to avoid warnings
y = data_clean[target].copy()    # Create a copy to avoid warnings

# --- Calculate K and L_1 ---
def calculate_k(masses):
    """Calculates the normalization constant K."""
    m0 = np.median(masses)
    sum_mi_m0 = np.sum(masses / m0)
    sum_m0_mi = np.sum(m0 / masses)
    return sum_mi_m0 / sum_m0_mi

def cosmological_l_function(data, s):
    """Computes the cosmological L-function."""
    logmass_values = data['logmstar'].values  # Using 'logmstar' as logmass
    l_value = np.sum((logmass_values / np.median(logmass_values))**(-s))
    return l_value

# Ensure 'logmstar' data is available for L-function calculation
masses = data_clean['logmstar'].values
K = calculate_k(masses)
print(f"Normalization constant K: {K:.4f}")

L_1 = cosmological_l_function(data_clean, 1)
print(f"L-function at s=1: {L_1:.4f}")

# --- Estimate Rank ---
def estimate_rank(data):
    """Estimates the rank of the galaxy distribution."""
    l_at_1 = cosmological_l_function(data, 1)
    l_at_1_plus_delta = cosmological_l_function(data, 1.001)
    derivative = (l_at_1_plus_delta - l_at_1) / 0.001
    return 1 if np.abs(derivative) > 1e-5 else 2

rank = estimate_rank(data_clean)
print(f"Estimated rank: {rank}")

# --- Add L_1 to features ---
# Calculate the average L_1 value to ensure it's a scalar
L_1_avg = np.mean(L_1)
X['L_1'] = L_1_avg  # Add L_1 as a new feature


# --- Split Data into Training and Testing Sets ---
print("Splitting data into training and testing sets...")
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

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
# Residual Plot for Random Forest
plt.figure(figsize=(8, 6))
residuals_rf = y_test - y_pred_rf
plt.scatter(y_pred_rf, residuals_rf, alpha=0.5)
plt.axhline(0, color='red', linestyle='--')
plt.xlabel('Predicted SFR')
plt.ylabel('Residuals')
plt.title('Residuals vs Predicted SFR (Random Forest)')
plt.show()

# Feature Importance for Random Forest
plt.figure(figsize=(8, 6))
importances = rf.feature_importances_
feature_names = X.columns
sorted_idx = importances.argsort()
plt.barh(feature_names[sorted_idx], importances[sorted_idx])
plt.xlabel('Importance')
plt.title('Feature Importances (Random Forest)')
plt.show()
