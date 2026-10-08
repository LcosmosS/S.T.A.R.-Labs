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

# --- Merge Datasets ---
print("Merging datasets on 'CATAID'...")
data = pd.merge(magphys, stellar_masses, on='CATAID', how='inner')
data = pd.merge(data, galaxies_classified, on='CATAID', how='inner')
data = pd.merge(data, environment_measures, on='CATAID', how='inner')

# --- Feature Engineering ---
print("Engineering features...")
data['log_mass_stellar'] = np.log10(data['mass_stellar_best_fit'])
data['log_sSFR'] = np.log10(data['sSFR_0_1Gyr_best_fit'] + 1e-6)
data['log_dust_mass'] = np.log10(data['mass_dust_best_fit'] + 1e-6)
data['log_Z'] = np.log10(data['metalicity_Z_Zo_percentile50'] + 1e-6)

# BSD-inspired feature
data['BSD_likelihood'] = data['log_mass_stellar'] * data['log_Z'] / (data['agem_percentile50'] + 1)

# --- Define Features and Target ---
features = [
    'log_mass_stellar', 'log_sSFR', 'log_dust_mass', 'log_Z', 'BSD_likelihood',
    'L_dust_best_fit', 'tau_V_best_fit', 'logmstar', 'extBV', 'gminusi', 'uminusr',
    'Z', 'GeoS4', 'GeoS10', 'DistanceTo5nn', 'SurfaceDensity', 'CountInCyl', 'AGEDenPar'
]
target = 'SFR_0_1Gyr_best_fit'

# --- Quality Filtering ---
print("Applying quality control filters...")
data = data[data['tau_V_best_fit'] > 0.1]  # Remove optically thin

# --- Drop NA and Split ---
print("Cleaning data and splitting...")
data_clean = data.dropna(subset=[target] + features)
X = data_clean[features]
y = data_clean[target]
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# --- Train Models ---
print("Training models...")
gb = GradientBoostingRegressor(random_state=42)
rf = RandomForestRegressor(random_state=42)
gb.fit(X_train, y_train)
rf.fit(X_train, y_train)

# --- Evaluate ---
y_pred_gb = gb.predict(X_test)
y_pred_rf = rf.predict(X_test)
mse_gb = mean_squared_error(y_test, y_pred_gb)
r2_gb = r2_score(y_test, y_pred_gb)
mse_rf = mean_squared_error(y_test, y_pred_rf)
r2_rf = r2_score(y_test, y_pred_rf)

print("\nModel Performance on Test Set:")
print(f"Gradient Boosting - MSE: {mse_gb:.4f}, R^2: {r2_gb:.4f}")
print(f"Random Forest     - MSE: {mse_rf:.4f}, R^2: {r2_rf:.4f}")

# --- Cross-Validation ---
print("\n5-Fold Cross-Validation:")
cv_mse_gb = -cross_val_score(gb, X, y, cv=5, scoring='neg_mean_squared_error').mean()
cv_r2_gb = cross_val_score(gb, X, y, cv=5, scoring='r2').mean()
cv_mse_rf = -cross_val_score(rf, X, y, cv=5, scoring='neg_mean_squared_error').mean()
cv_r2_rf = cross_val_score(rf, X, y, cv=5, scoring='r2').mean()

print(f"Gradient Boosting - CV MSE: {cv_mse_gb:.4f}, R^2: {cv_r2_gb:.4f}")
print(f"Random Forest     - CV MSE: {cv_mse_rf:.4f}, R^2: {cv_r2_rf:.4f}")

# --- Plot BSD Likelihood vs SFR ---
plt.figure(figsize=(8, 6))
plt.scatter(data_clean['BSD_likelihood'], data_clean[target], alpha=0.5, c='blue')
plt.xlabel('BSD Likelihood (symbolic)')
plt.ylabel('Star Formation Rate (SFR)')
plt.title('BSD-inspired Metric vs SFR')
plt.grid(True)
plt.show()
# --- SHAP: Explain Gradient Boosting Model ---
import shap

print("\nRunning SHAP for Gradient Boosting...")
explainer = shap.Explainer(gb, X_train)
shap_values = explainer(X_test)

# Summary Plot
shap.summary_plot(shap_values, X_test, plot_type="bar")

# Full detailed plot (optional but insightful)
shap.summary_plot(shap_values, X_test)

# --- Symbolic Regression with PySR ---
from pysr import PySRRegressor

print("\nRunning symbolic regression with PySR...")
symbolic_model = PySRRegressor(
    model_selection="best",  # Use best validation loss
    niterations=100,
    binary_operators=["+", "-", "*", "/"],
    unary_operators=["cos", "sin", "exp", "log", "sqrt"],
    loss="loss(x, y) = (x - y)^2",
    maxsize=20,
    verbosity=1,
)

symbolic_model.fit(X_train.values, y_train.values)

# Print best symbolic expression
print("\nBest symbolic equation:")
print(symbolic_model)

# Optionally plot loss vs complexity
symbolic_model.plot()
