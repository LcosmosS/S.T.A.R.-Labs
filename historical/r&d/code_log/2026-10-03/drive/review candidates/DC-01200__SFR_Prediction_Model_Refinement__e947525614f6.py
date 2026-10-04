import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import GradientBoostingRegressor, RandomForestRegressor
from sklearn.metrics import mean_squared_error, r2_score
import matplotlib.pyplot as plt
import shap


# --- Load SDSS DR18 Dataset ---
sdss_path = '/path/to/SDSSDR18_200000.csv'  # Update with the correct path
df_sdss = pd.read_csv(sdss_path)


# Display column names to understand structure
print("Columns in SDSS dataset:", df_sdss.columns)


# --- Preprocess the Data ---
# Let's select some key columns
features_sdss = ['ra', 'dec', 'u', 'g', 'r', 'i', 'z', 'redshift', 'plate', 'mjd']
target_sdss = 'redshift'  # Assuming we want to predict redshift, replace with other targets if needed


# Drop rows with missing values
df_sdss_clean = df_sdss[features_sdss + [target_sdss]].dropna()


# --- Feature and Target Variables ---
X_sdss = df_sdss_clean[features_sdss]
y_sdss = df_sdss_clean[target_sdss]


# --- Scale Features ---
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X_sdss)


# --- Split Data into Training and Test Sets ---
X_train, X_test, y_train, y_test = train_test_split(X_scaled, y_sdss, test_size=0.2, random_state=42)


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
mse_gb = mean_squared_error(y_test, y_pred_gb)
r2_gb = r2_score(y_test, y_pred_gb)
mse_rf = mean_squared_error(y_test, y_pred_rf)
r2_rf = r2_score(y_test, y_pred_rf)


print("\nModel Performance on Test Set:")
print(f"Gradient Boosting - MSE: {mse_gb:.4f}, R²: {r2_gb:.4f}")
print(f"Random Forest - MSE: {mse_rf:.4f}, R²: {r2_rf:.4f}")


# --- Perform 5-Fold Cross-Validation ---
print("\nPerforming 5-fold cross-validation...")
from sklearn.model_selection import cross_val_score
cv_mse_gb = -cross_val_score(gb, X_sdss, y_sdss, cv=5, scoring='neg_mean_squared_error').mean()
cv_r2_gb = cross_val_score(gb, X_sdss, y_sdss, cv=5, scoring='r2').mean()
cv_mse_rf = -cross_val_score(rf, X_sdss, y_sdss, cv=5, scoring='neg_mean_squared_error').mean()
cv_r2_rf = cross_val_score(rf, X_sdss, y_sdss, cv=5, scoring='r2').mean()


print(f"Cross-Validation MSE (Gradient Boosting): {cv_mse_gb:.4f}, R²: {cv_r2_gb:.4f}")
print(f"Cross-Validation MSE (Random Forest): {cv_mse_rf:.4f}, R²: {cv_r2_rf:.4f}")


# --- SHAP Summary Plot for Model Interpretability ---
explainer = shap.Explainer(gb, X_train)
shap_values = explainer(X_test)
shap.summary_plot(shap_values, X_test, plot_type="bar")


# --- Save Feature Importances Plot ---
plt.figure(figsize=(8, 6))
importances = rf.feature_importances_
feature_names = X_sdss.columns
sorted_idx = importances.argsort()
plt.barh(feature_names[sorted_idx], importances[sorted_idx])
plt.xlabel('Importance')
plt.title('Feature Importances (Random Forest)')
plt.savefig('feature_importances_sdss.png')


# --- Save Residual Plot ---
plt.figure(figsize=(8, 6))
residuals_rf = y_test - y_pred_rf
plt.scatter(y_pred_rf, residuals_rf, alpha=0.5)
plt.axhline(0, color='red', linestyle='--')
plt.xlabel('Predicted Redshift')
plt.ylabel('Residuals')
plt.title('Residuals vs Predicted Redshift (Random Forest)')
plt.savefig('residuals_plot_sdss.png')
