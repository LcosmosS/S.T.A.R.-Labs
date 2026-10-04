import pandas as pd from sklearn.model_selection import train_test_split from sklearn.ensemble import GradientBoostingRegressor, RandomForestRegressor from sklearn.metrics import mean_squared_error, r2_score import matplotlib.pyplot as plt
# --- Correct Data Paths ---
pipe3d_path = '/mnt/data/pipe3d_data.csv' # Adjusted path for WSL magphys_path = '/mnt/data/MagPhys.csv' # Adjusted path for WSL stellar_masses_path = '/mnt/data/Stellar_Mass2_Table.csv' # Adjusted path for WSL environment_measures_path = '/mnt/data/EnvironmentMeasures.csv' # Adjusted path for WSL
# --- Load Datasets ---
print("Loading datasets...") df_main = pd.read_csv(pipe3d_path) df_magphys = pd.read_csv(magphys_path) df_stellar = pd.read_csv(stellar_masses_path) df_env = pd.read_csv(environment_measures_path)
# --- Feature Selection --- # Assuming these are the relevant columns for our analysis
features = ['log_Mass_gas', 'log_SFR_Ha', 'log_Mass', 'log_SFR_ssp', 'mass_stellar_best_fit'] target = 'SFR_0_1Gyr_best_fit'
# --- Filter and Clean Data --- # Filter relevant columns and remove any rows with missing values
df_main_clean = df_main[['CATAID'] + features + [target]].dropna()
# --- Train-Test Split ---
X = df_main_clean[features] y = df_main_clean[target]
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
# --- Model Training ---
print("Training models...")
# Gradient Boosting Regressor
gb = GradientBoostingRegressor(random_state=42) gb.fit(X_train, y_train)
# Random Forest Regressor
rf = RandomForestRegressor(random_state=42) rf.fit(X_train, y_train)
# --- Predictions ---
y_pred_gb = gb.predict(X_test) y_pred_rf = rf.predict(X_test)
# --- Model Evaluation ---
mse_gb = mean_squared_error(y_test, y_pred_gb) r2_gb = r2_score(y_test, y_pred_gb) mse_rf = mean_squared_error(y_test, y_pred_rf) r2_rf = r2_score(y_test, y_pred_rf)
print(f"Gradient Boosting - MSE: {mse_gb:.4f}, R²: {r2_gb:.4f}") print(f"Random Forest - MSE: {mse_rf:.4f}, R²: {r2_rf:.4f}")
# --- Visualize Results --- # Residual Plot for Gradient Boosting
plt.figure(figsize=(8, 6)) residuals_gb = y_test - y_pred_gb plt.scatter(y_pred_gb, residuals_gb, alpha=0.5) plt.axhline(0, color='red', linestyle='--') plt.xlabel('Predicted SFR') plt.ylabel('Residuals') plt.title('Residuals vs Predicted SFR (Gradient Boosting)') plt.show()
# Feature Importance for Random Forest
plt.figure(figsize=(8, 6)) importances = rf.feature_importances_ feature_names = X.columns sorted_idx = importances.argsort() plt.barh(feature_names[sorted_idx], importances[sorted_idx]) plt.xlabel('Importance') plt.title('Feature Importances (Random Forest)') plt.show()
