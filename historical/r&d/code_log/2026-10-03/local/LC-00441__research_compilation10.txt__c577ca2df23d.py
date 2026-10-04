import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import PolynomialFeatures
from sklearn.metrics import mean_squared_error, r2_score
import matplotlib.pyplot as plt


# --- 1. Data Preparation ---
# Load dataset
df = pd.read_csv('merged_data.csv')
print(f"Dataset loaded with {len(df)} rows and {len(df.columns)} columns.")


# Replace sentinel values with NaN
df = df.replace(-9999, np.nan)


# Define target and features
target = 'log_SFR_Ha'
base_features = ['log_Mass_gas', 'nsa_mstar', 'log_Mass', 'V-band_SB_at_Re', 
                 'vel_sigma_Re', 'OH_Mar13_N2_Re_fit', 'Av_gas_Re']


# Impute missing values with median
imputer = SimpleImputer(strategy='median')
df[base_features] = imputer.fit_transform(df[base_features])


# Drop rows with missing target
df = df.dropna(subset=[target])
y = df[target]
X = df[base_features]


# --- 2. Feature Engineering ---
# Add interaction and nonlinear terms
df['log_Mass_gas_times_nsa_mstar'] = df['log_Mass_gas'] * df['nsa_mstar']
df['log_Mass_gas_times_metallicity'] = df['log_Mass_gas'] * df['OH_Mar13_N2_Re_fit']
df['log_Mass_gas_squared'] = df['log_Mass_gas'] ** 2


# Generate polynomial features
poly = PolynomialFeatures(degree=2, include_bias=False)
X_poly = poly.fit_transform(X)
feature_names = poly.get_feature_names_out(base_features)


# --- 3. Initial Model for Outlier Detection ---
# Split data
X_train, X_test, y_train, y_test = train_test_split(X_poly, y, test_size=0.2, random_state=42)


# Train initial Random Forest to identify outliers
initial_model = RandomForestRegressor(random_state=42)
initial_model.fit(X_train, y_train)
y_pred_initial = initial_model.predict(X_test)


# Identify outliers based on residuals
residuals = y_test - y_pred_initial
outlier_threshold = 2
outliers = np.abs(residuals) > outlier_threshold
non_outliers = ~outliers


# --- 4. Adjust Models for Outliers ---
# Define sample weights for Random Forest (down-weight outliers)
sample_weights = np.ones(len(y_train))
sample_weights[np.abs(y_train - initial_model.predict(X_train)) > outlier_threshold] = 0.5


# --- 5. Train and Tune Models ---
# Hyperparameter grids
rf_param_grid = {
    'n_estimators': [100, 200],
    'max_depth': [10, 20],
    'min_samples_split': [5, 10]
}


gb_param_grid = {
    'learning_rate': [0.05, 0.1],
    'max_depth': [5, 7],
    'n_estimators': [100, 200],
    'loss': ['huber']  # Robust to outliers
}


# Initialize models
rf = RandomForestRegressor(random_state=42)
gb = GradientBoostingRegressor(random_state=42)


# Tune Random Forest with sample weights
rf_grid = GridSearchCV(rf, rf_param_grid, cv=5, scoring='neg_mean_squared_error', n_jobs=-1)
rf_grid.fit(X_train, y_train, sample_weight=sample_weights)
best_rf = rf_grid.best_estimator_


# Tune Gradient Boosting
gb_grid = GridSearchCV(gb, gb_param_grid, cv=5, scoring='neg_mean_squared_error', n_jobs=-1)
gb_grid.fit(X_train, y_train)
best_gb = gb_grid.best_estimator_


# --- 6. Evaluate Models ---
def evaluate_model(model, X_test, y_test, outliers, non_outliers):
    y_pred = model.predict(X_test)
    mse_full = mean_squared_error(y_test, y_pred)
    r2_full = r2_score(y_test, y_pred)
    mse_outliers = mean_squared_error(y_test[outliers], y_pred[outliers])
    r2_outliers = r2_score(y_test[outliers], y_pred[outliers])
    mse_non_outliers = mean_squared_error(y_test[non_outliers], y_pred[non_outliers])
    r2_non_outliers = r2_score(y_test[non_outliers], y_pred[non_outliers])
    return mse_full, r2_full, mse_outliers, r2_outliers, mse_non_outliers, r2_non_outliers


# Evaluate Random Forest
rf_results = evaluate_model(best_rf, X_test, y_test, outliers, non_outliers)
print("\nRandom Forest Results:")
print(f"Full Test Set - MSE: {rf_results[0]:.4f}, R-squared: {rf_results[1]:.4f}")
print(f"Outliers - MSE: {rf_results[2]:.4f}, R-squared: {rf_results[3]:.4f}")
print(f"Non-Outliers - MSE: {rf_results[4]:.4f}, R-squared: {rf_results[5]:.4f}")


# Evaluate Gradient Boosting
gb_results = evaluate_model(best_gb, X_test, y_test, outliers, non_outliers)
print("\nGradient Boosting Results:")
print(f"Full Test Set - MSE: {gb_results[0]:.4f}, R-squared: {gb_results[1]:.4f}")
print(f"Outliers - MSE: {gb_results[2]:.4f}, R-squared: {gb_results[3]:.4f}")
print(f"Non-Outliers - MSE: {gb_results[4]:.4f}, R-squared: {gb_results[5]:.4f}")


# --- 7. Visualize Residuals ---
# Random Forest residuals
y_pred_rf = best_rf.predict(X_test)
residuals_rf = y_test - y_pred_rf
plt.figure(figsize=(8, 6))
plt.scatter(y_pred_rf, residuals_rf, alpha=0.5)
plt.axhline(0, color='red', linestyle='--')
plt.xlabel('Predicted log_SFR_Ha')
plt.ylabel('Residuals')
plt.title('Residuals vs. Predicted (Random Forest)')
plt.savefig('residuals_rf.png')
plt.close()


# Gradient Boosting residuals
y_pred_gb = best_gb.predict(X_test)
residuals_gb = y_test - y_pred_gb
plt.figure(figsize=(8, 6))
plt.scatter(y_pred_gb, residuals_gb, alpha=0.5)
plt.axhline(0, color='red', linestyle='--')
plt.xlabel('Predicted log_SFR_Ha')
plt.ylabel('Residuals')
plt.title('Residuals vs. Predicted (Gradient Boosting)')
plt.savefig('residuals_gb.png')
plt.close()
print("Residual plots saved as 'residuals_rf.png' and 'residuals_gb.png'.")


# --- 8. Feature Importance ---
# Random Forest
importances_rf = best_rf.feature_importances_
importance_df_rf = pd.DataFrame({'Feature': feature_names, 'Importance': importances_rf})
print("\nTop 10 Important Features (Random Forest):")
print(importance_df_rf.sort_values(by='Importance', ascending=False).head(10))


# Gradient Boosting
importances_gb = best_gb.feature_importances_
importance_df_gb = pd.DataFrame({'Feature': feature_names, 'Importance': importances_gb})
print("\nTop 10 Important Features (Gradient Boosting):")
print(importance_df_gb.sort_values(by='Importance', ascending=False).head(10))
