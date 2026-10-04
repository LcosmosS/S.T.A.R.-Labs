import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.ensemble import GradientBoostingRegressor, RandomForestRegressor
from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt
import shap
from pysr import PySRRegressor


# --- Load Datasets ---
print("Loading datasets...")
pipe3d_data_path = '/mnt/data/pipe3d_data.csv'  # Update with the correct path
df_main = pd.read_csv(pipe3d_data_path)


# --- Select Additional Features for Enhanced Model ---
features = [
    'log_Mass_gas', 'log_SFR_SF', 'log_Mass', 'Re_kpc', 'Age_LW_Re_fit', 
    'log_NII_Ha_cen', 'log_SFR_ssp', 'OH_O3N2_cen', 'log_SFR_D_C', 
    'mass_stellar_best_fit', 'metalicity_Z_Zo_percentile50', 'log_SFR_Ha'
]


target = 'SFR_0_1Gyr_best_fit'


# --- Filter Columns and Drop Missing Values ---
df_main_clean = df_main[['CATAID'] + features + [target]].dropna()


# --- Feature and Target Variables ---
X = df_main_clean[features]
y = df_main_clean[target]


# --- Scale Features ---
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)


# --- Split Data into Training and Test Sets ---
X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.2, random_state=42)


# --- Train Models ---
# Train Gradient Boosting Model
print("Training Gradient Boosting model...")
gb = GradientBoostingRegressor(random_state=42)
gb.fit(X_train, y_train)


# Train Random Forest Model
print("Training Random Forest model...")
rf = RandomForestRegressor(random_state=42)
rf.fit(X_train, y_train)


# --- Make Predictions ---
y_pred_gb = gb.predict(X_test)
y_pred_rf = rf.predict(X_test)


# --- Evaluate Models ---
from sklearn.metrics import mean_squared_error, r2_score
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


# --- SHAP Summary Plot for Model Interpretability ---
explainer = shap.Explainer(gb, X_train)
shap_values = explainer(X_test)
shap.summary_plot(shap_values, X_test, plot_type="bar")


# --- Symbolic Regression with PySR ---
print("\nRunning symbolic regression with PySR...")
symbolic_regressor = PySRRegressor(
    niterations=1000,
    model="additive",
    verbosity=1
)
symbolic_regressor.fit(X_train, y_train)


# Display symbolic regression result
print("Best symbolic model: ", symbolic_regressor)


# Save the model
symbolic_regressor.save("best_model_symbregressor")


# --- Save Residual Plot ---
plt.figure(figsize=(8, 6))
residuals_rf = y_test - y_pred_rf
plt.scatter(y_pred_rf, residuals_rf, alpha=0.5)
plt.axhline(0, color='red', linestyle='--')
plt.xlabel('Predicted SFR')
plt.ylabel('Residuals')
plt.title('Residuals vs Predicted SFR (Random Forest)')
plt.savefig('/home/pmqr7/residuals_plot.png')


# --- Save Feature Importances Plot ---
plt.figure(figsize=(8, 6))
importances = rf.feature_importances_
feature_names = X.columns
sorted_idx = importances.argsort()
plt.barh(feature_names[sorted_idx], importances[sorted_idx])
plt.xlabel('Importance')
plt.title('Feature Importances (Random Forest)')
plt.savefig('/home/pmqr7/feature_importances_plot.png')
