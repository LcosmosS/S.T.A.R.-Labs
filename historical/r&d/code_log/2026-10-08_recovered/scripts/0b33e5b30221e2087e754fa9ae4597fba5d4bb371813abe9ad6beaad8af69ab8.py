import pandas as pd
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.ensemble import GradientBoostingRegressor, RandomForestRegressor
from sklearn.metrics import mean_squared_error, r2_score
import matplotlib.pyplot as plt

# --- Load Datasets ---
print("Loading datasets...")
magphys = pd.read_csv('MagPhys.csv')
stellar_masses = pd.read_csv('StellarMassesLambdar.csv')

# --- Merge Datasets on 'CATAID' ---
print("Merging datasets on 'CATAID'...")
data = pd.merge(magphys, stellar_masses, on='CATAID', how='inner')

# --- Define Relevant Features and Target ---
# Only include features relevant to the analysis, ignoring all other columns
features = [
    'mass_stellar_best_fit',       # Stellar mass best fit from MagPhys
    'sSFR_0_1Gyr_best_fit',        # Specific SFR over the last 0.1 Gyr from MagPhys
    'L_dust_best_fit',             # Dust luminosity from MagPhys
    'tau_V_best_fit',              # Optical depth from MagPhys
    'mass_dust_best_fit',          # Dust mass from MagPhys
    'metalicity_Z_Zo_percentile50',# Metallicity (50th percentile) from MagPhys
    'agem_percentile50',           # Stellar age (50th percentile) from MagPhys
    'logmstar',                    # Log stellar mass from StellarMassesLambdar
    'extBV',                       # Extinction in B-V from StellarMassesLambdar
    'gminusi',                     # g-i color index from StellarMassesLambdar
    'uminusr'                      # u-r color index from StellarMassesLambdar
]

# Target variable: SFR over the last 0.1 Gyr from MagPhys
target = 'SFR_0_1Gyr_best_fit'

# --- Clean Data ---
# Drop rows with missing values in target or features
print("Cleaning data...")
data_clean = data.dropna(subset=[target] + features)
print(f"Dataset size after cleaning: {data_clean.shape[0]} rows")

# Extract features (X) and target (y)
X = data_clean[features]
y = data_clean[target]

# --- Split Data into Training and Testing Sets ---
print("Splitting data into training and testing sets...")
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# --- Train Models ---
# Gradient Boosting Regressor
print("Training Gradient Boosting model...")
gb = GradientBoostingRegressor(random_state=42)
gb.fit(X_train, y_train)

# Random Forest Regressor
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