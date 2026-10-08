import pandas as pd
import shap
import matplotlib.pyplot as plt
from sklearn.ensemble import GradientBoostingRegressor, RandomForestRegressor
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.metrics import mean_squared_error, r2_score
from pysr import PySRRegressor

# --- Load & Merge Datasets ---
magphys = pd.read_csv('MagPhys.csv')[['CATAID', 'mass_stellar_best_fit', 'sSFR_0_1Gyr_best_fit',
                                      'L_dust_best_fit', 'tau_V_best_fit', 'mass_dust_best_fit',
                                      'metalicity_Z_Zo_percentile50', 'agem_percentile50', 'SFR_0_1Gyr_best_fit']]
stellar_masses = pd.read_csv('StellarMassesLambdar.csv')[['CATAID', 'logmstar', 'extBV', 'gminusi', 'uminusr']]
galaxies_classified = pd.read_csv('GalaxiesClassified.csv')[['CATAID', 'Z', 'GeoS4', 'GeoS10']]
environment_measures = pd.read_csv('EnvironmentMeasures.csv')[['CATAID', 'DistanceTo5nn', 'SurfaceDensity',
                                                               'CountInCyl', 'AGEDenPar']]

# --- Merge ---
data = pd.merge(magphys, stellar_masses, on='CATAID')
data = pd.merge(data, galaxies_classified, on='CATAID')
data = pd.merge(data, environment_measures, on='CATAID')

# --- Features & Target ---
features = [
    'mass_stellar_best_fit', 'sSFR_0_1Gyr_best_fit', 'L_dust_best_fit', 'tau_V_best_fit',
    'mass_dust_best_fit', 'metalicity_Z_Zo_percentile50', 'agem_percentile50',
    'logmstar', 'extBV', 'gminusi', 'uminusr', 'Z', 'GeoS4', 'GeoS10',
    'DistanceTo5nn', 'SurfaceDensity', 'CountInCyl', 'AGEDenPar'
]
target = 'SFR_0_1Gyr_best_fit'

# --- Clean Data ---
data_clean = data.dropna(subset=[target] + features)
X = data_clean[features]
y = data_clean[target]

# --- Split Data ---
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# --- Train Models ---
gb = GradientBoostingRegressor(random_state=42).fit(X_train, y_train)
rf = RandomForestRegressor(random_state=42).fit(X_train, y_train)

# --- Evaluation ---
print("\nTest R² Scores:")
print(f"Gradient Boosting: {r2_score(y_test, gb.predict(X_test)):.4f}")
print(f"Random Forest    : {r2_score(y_test, rf.predict(X_test)):.4f}")

# --- SHAP Interpretability ---
print("\nGenerating SHAP plots...")
explainer = shap.Explainer(gb)
shap_values = explainer(X)

# Summary Plot (Global Importance)
shap.summary_plot(shap_values, X)

# Dependence Plot (e.g., metallicity)
shap.dependence_plot("metalicity_Z_Zo_percentile50", shap_values.values, X)

# --- Symbolic Regression with PySR ---
print("\nRunning symbolic regression...")
X_pysr = X.copy()
X_pysr.columns = [f"x{i}" for i in range(X.shape[1])]  # PySR expects generic names
model = PySRRegressor(
    niterations=100,
    binary_operators=["+", "-", "*", "/", "pow"],
    unary_operators=["log", "sqrt", "exp", "abs"],
    model_selection="best",
    loss="loss(x, y) = (x - y)^2",
    maxsize=20,
    verbosity=1,
)
model.fit(X_pysr, y.values)

# Show symbolic equations
print("\nDiscovered Equations:")
print(model)

# Optionally plot complexity vs accuracy
model.plot()
