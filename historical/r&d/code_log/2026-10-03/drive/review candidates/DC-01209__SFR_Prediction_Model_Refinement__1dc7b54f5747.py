import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import GradientBoostingRegressor, RandomForestRegressor
from sklearn.metrics import mean_squared_error, r2_score
import matplotlib.pyplot as plt
import numpy as np


# --- Load the Dataset ---
print("Loading dataset...")
df = pd.read_csv('/path/to/StellarMassesLambdar.csv')  # Update with your actual file path


# --- Select random features from the dataset ---
# List of features you provided. We'll select a random subset of these.
features = [
    'Z', 'nQ', 'SURVEY_CODE', 'SURVEY_CLASS', 'Z_TONRY', 'fluxscale', 'zmax_19p8', 'zmax_19p4', 'nbands', 
    'S2N', 'PPP', 'logmstar', 'dellogmstar', 'logage', 'dellogage', 'logtau', 'logmintsfh', 'logmremnants',
    'metal', 'delmetal', 'extBV', 'delextBV', 'logLWage', 'dellogLWage', 'gminusi', 'delgminusi', 'uminusr',
    'deluminusr', 'gminusi_stars', 'uminusr_stars', 'C_logM_ur', 'C_logM_gi', 'C_logM_eBV', 'absmag_u', 
    'absmag_g', 'absmag_r', 'absmag_i', 'absmag_z', 'fitphot_u', 'fitphot_g', 'fitphot_r', 'fitphot_i', 
    'fitphot_z', 'fitphot_X', 'absmag_X', 'absmag_Y', 'absmag_J', 'absmag_H', 'absmag_K'
]


# Randomly sample 6 features from the list of available features
np.random.seed(42)  # Set seed for reproducibility
random_features = np.random.choice(features, size=6, replace=False)
print(f"Selected features for training: {random_features}")


# Target variable: Predicting 'logmstar' (log of stellar mass)
target = 'logmstar'


# --- Clean Data ---
print("Cleaning data...")
# Dropping rows with missing values for the selected features and target
df_clean = df[list(random_features) + [target]].dropna()
print(f"Dataset size after cleaning: {df_clean.shape[0]} rows")


# --- Split Data into Training and Testing Sets ---
print("Splitting data into training and testing sets...")
X = df_clean[random_features]
y = df_clean[target]


X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)


print(f"Training set size: {X_train.shape[0]} rows")
print(f"Test set size: {X_test.shape[0]} rows")


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
plt.xlabel('Predicted logmstar')
plt.ylabel('Residuals')
plt.title('Residuals vs Predicted logmstar (Random Forest)')
plt.show()


# Feature Importance for Random Forest
plt.figure(figsize=(8, 6))
importances = rf.feature_importances_
sorted_idx = importances.argsort()
plt.barh(random_features[sorted_idx], importances[sorted_idx])
plt.xlabel('Importance')
plt.title('Feature Importances (Random Forest)')
plt.show()
