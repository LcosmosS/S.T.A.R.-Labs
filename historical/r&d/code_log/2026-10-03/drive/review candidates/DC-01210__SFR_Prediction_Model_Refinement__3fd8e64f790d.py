import pandas as pd
from sklearn.model_selection import train_test_split, GridSearchCV, RandomizedSearchCV
from sklearn.ensemble import GradientBoostingRegressor, RandomForestRegressor
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import mean_squared_error, r2_score
import matplotlib.pyplot as plt
import numpy as np


# --- Load the Dataset ---
print("Loading dataset...")
df = pd.read_csv('/path/to/StellarMassesLambdar.csv')  # Update with your actual file path


# --- Select random features from the dataset ---
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


# --- Scale the Features ---
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)


# --- Hyperparameter Tuning for Random Forest ---
print("Tuning Random Forest model...")
rf = RandomForestRegressor(random_state=42)
rf_param_grid = {
    'n_estimators': [100, 200, 300],
    'max_depth': [None, 10, 20, 30],
    'min_samples_split': [2, 5, 10],
    'min_samples_leaf': [1, 2, 4]
}
rf_random_search = RandomizedSearchCV(rf, param_distributions=rf_param_grid, n_iter=10, cv=5, verbose=1, random_state=42, n_jobs=-1)
rf_random_search.fit(X_train_scaled, y_train)


print(f"Best Random Forest parameters: {rf_random_search.best_params_}")
rf_best = rf_random_search.best_estimator_


# --- Hyperparameter Tuning for Gradient Boosting ---
print("Tuning Gradient Boosting model...")
gb = GradientBoostingRegressor(random_state=42)
gb_param_grid = {
    'n_estimators': [100, 200, 300],
    'learning_rate': [0.01, 0.1, 0.2],
    'max_depth': [3, 5, 7],
    'subsample': [0.8, 0.9, 1.0]
}
gb_grid_search = GridSearchCV(gb, param_grid=gb_param_grid, cv=5, verbose=1, n_jobs=-1)
gb_grid_search.fit(X_train_scaled, y_train)


print(f"Best Gradient Boosting parameters: {gb_grid_search.best_params_}")
gb_best = gb_grid_search.best_estimator_


# --- Make Predictions ---
y_pred_rf = rf_best.predict(X_test_scaled)
y_pred_gb = gb_best.predict(X_test_scaled)


# --- Evaluate Models on Test Set ---
mse_rf = mean_squared_error(y_test, y_pred_rf)
r2_rf = r2_score(y_test, y_pred_rf)
mse_gb = mean_squared_error(y_test, y_pred_gb)
r2_gb = r2_score(y_test, y_pred_gb)


print("\nModel Performance on Test Set:")
print(f"Random Forest - MSE: {mse_rf:.4f}, R²: {r2_rf:.4f}")
print(f"Gradient Boosting - MSE: {mse_gb:.4f}, R²: {r2_gb:.4f}")


# --- Visualize Results ---
# Feature Importance for Random Forest
plt.figure(figsize=(8, 6))
importances_rf = rf_best.feature_importances_
sorted_idx_rf = importances_rf.argsort()
plt.barh(random_features[sorted_idx_rf], importances_rf[sorted_idx_rf])
plt.xlabel('Importance')
plt.title('Feature Importances (Random Forest)')
plt.show()


# Feature Importance for Gradient Boosting
plt.figure(figsize=(8, 6))
importances_gb = gb_best.feature_importances_
sorted_idx_gb = importances_gb.argsort()
plt.barh(random_features[sorted_idx_gb], importances_gb[sorted_idx_gb])
plt.xlabel('Importance')
plt.title('Feature Importances (Gradient Boosting)')
plt.show()
