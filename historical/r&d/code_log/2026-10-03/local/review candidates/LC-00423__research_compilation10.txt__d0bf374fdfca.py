import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.model_selection import train_test_split, GridSearchCV, KFold
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import PolynomialFeatures
from sklearn.metrics import mean_squared_error, r2_score
import matplotlib.pyplot as plt


# --- 1. Data Preparation ---
# Load dataset
df = pd.read_csv('compiled_sfr_dataset.csv')
print(f"Dataset loaded with {len(df)} rows and {len(df.columns)} columns.")


# Replace sentinel values with NaN
df = df.replace(-9999, np.nan)


# Define target and features
target = 'log_SFR_Ha'
features = ['log_Mass_gas', 'nsa_mstar', 'log_Mass', 'vel_sigma_Re', 
            'OH_Mar13_N2_Re_fit', 'Av_gas_Re', 'zcomp_1Mpc', 'LOGMSTARS', 'SFR_PETRORAD_R']


# Impute missing values with median
imputer = SimpleImputer(strategy='median')
df[features] = imputer.fit_transform(df[features])


# Drop rows with missing target
df = df.dropna(subset=[target])
y = df[target]
X = df[features]


# --- 2. Feature Engineering ---
# Add interaction and nonlinear terms
df['log_Mass_gas_times_nsa_mstar'] = df['log_Mass_gas'] * df['nsa_mstar']
df['log_Mass_gas_times_metallicity'] = df['log_Mass_gas'] * df['OH_Mar13_N2_Re_fit']
df['log_Mass_gas_squared'] = df['log_Mass_gas'] ** 2
df['log_Mass_gas_times_zcomp'] = df['log_Mass_gas'] * df['zcomp_1Mpc']
df['LOGMSTARS_squared'] = df['LOGMSTARS'] ** 2


# Generate polynomial features
poly = PolynomialFeatures(degree=2, include_bias=False)
X_poly = poly.fit_transform(X)
feature_names = poly.get_feature_names_out(features)


# --- 3. Outlier Detection ---
# Identify outliers using IQR on target
Q1, Q3 = y.quantile(0.25), y.quantile(0.75)
IQR = Q3 - Q1
outliers = (y < Q1 - 1.5 * IQR) | (y > Q3 + 1.5 * IQR)
print(f"Number of outliers in target: {outliers.sum()}")


# --- 4. Model Training and Hyperparameter Tuning ---
# Split the data
X_train, X_test, y_train, y_test = train_test_split(X_poly, y, test_size=0.2, random_state=42)
print(f"Training set: {X_train.shape[0]} rows, Testing set: {X_test.shape[0]} rows")


# Random Forest hyperparameter grid
rf_params = {
    'n_estimators': [100, 200, 300],
    'max_depth': [10, 20, None],
    'min_samples_split': [2, 5, 10]
}
rf = RandomForestRegressor(random_state=42)
rf_grid = GridSearchCV(rf, rf_params, cv=5, scoring='neg_mean_squared_error')
rf_grid.fit(X_train, y_train)
best_rf = rf_grid.best_estimator_
print(f"Best RF hyperparameters: {rf_grid.best_params_}")


# Gradient Boosting hyperparameter grid
gb_params = {
    'learning_rate': [0.01, 0.05, 0.1],
    'max_depth': [3, 5, 7],
    'n_estimators': [100, 200, 300]
}
gb = GradientBoostingRegressor(random_state=42, loss='huber')
gb_grid = GridSearchCV(gb, gb_params, cv=5, scoring='neg_mean_squared_error')
gb_grid.fit(X_train, y_train)
best_gb = gb_grid.best_estimator_
print(f"Best GB hyperparameters: {gb_grid.best_params_}")


# --- 5. Model Evaluation ---
def evaluate_model(model, X_test, y_test, outliers, non_outliers):
    y_pred = model.predict(X_test)
    mse_full = mean_squared_error(y_test, y_pred)
    r2_full = r2_score(y_test, y_pred)
    mse_outliers = mean_squared_error(y_test[outliers], y_pred[outliers]) if outliers.sum() > 0 else np.nan
    r2_outliers = r2_score(y_test[outliers], y_pred[outliers]) if outliers.sum() > 0 else np.nan
    mse_non_outliers = mean_squared_error(y_test[non_outliers], y_pred[non_outliers])
    r2_non_outliers = r2_score(y_test[non_outliers], y_pred[non_outliers])
    return mse_full, r2_full, mse_outliers, r2_outliers, mse_non_outliers, r2_non_outliers


# Evaluate Random Forest
rf_results = evaluate_model(best_rf, X_test, y_test, outliers, ~outliers)
print("\nRandom Forest Results:")
print(f"Full Test Set - MSE: {rf_results[0]:.4f}, R-squared: {rf_results[1]:.4f}")
if not np.isnan(rf_results[2]):
    print(f"Outliers - MSE: {rf_results[2]:.4f}, R-squared: {rf_results[3]:.4f}")
print(f"Non-Outliers - MSE: {rf_results[4]:.4f}, R-squared: {rf_results[5]:.4f}")


# Evaluate Gradient Boosting
gb_results = evaluate_model(best_gb, X_test, y_test, outliers, ~outliers)
print("\nGradient Boosting Results:")
print(f"Full Test Set - MSE: {gb_results[0]:.4f}, R-squared: {gb_results[1]:.4f}")
if not np.isnan(gb_results[2]):
    print(f"Outliers - MSE: {gb_results[2]:.4f}, R-squared: {gb_results[3]:.4f}")
print(f"Non-Outliers - MSE: {gb_results[4]:.4f}, R-squared: {gb_results[5]:.4f}")


# --- 6. K-Fold Cross-Validation ---
kf = KFold(n_splits=5, shuffle=True, random_state=42)


# Random Forest cross-validation
rf_cv_mse = -cross_val_score(best_rf, X_poly, y, cv=kf, scoring='neg_mean_squared_error').mean()
rf_cv_r2 = cross_val_score(best_rf, X_poly, y, cv=kf, scoring='r2').mean()
print(f"\nRandom Forest K-Fold CV - Average MSE: {rf_cv_mse:.4f}, Average R-squared: {rf_cv_r2:.4f}")


# Gradient Boosting cross-validation
gb_cv_mse = -cross_val_score(best_gb, X_poly, y, cv=kf, scoring='neg_mean_squared_error').mean()
gb_cv_r2 = cross_val_score(best_gb, X_poly, y, cv=kf, scoring='r2').mean()
print(f"Gradient Boosting K-Fold CV - Average MSE: {gb_cv_mse:.4f}, Average R-squared: {gb_cv_r2:.4f}")


# --- 7. Visualization ---
# Residual plot for Random Forest
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


# Residual plot for Gradient Boosting
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


# --- 8. Feature Importance ---
# Random Forest
rf_importance = pd.DataFrame({'Feature': feature_names, 'Importance': best_rf.feature_importances_})
print("\nTop 10 Important Features (Random Forest):")
print(rf_importance.sort_values(by='Importance', ascending=False).head(10))


# Gradient Boosting
gb_importance = pd.DataFrame({'Feature': feature_names, 'Importance': best_gb.feature_importances_})
print("\nTop 10 Important Features (Gradient Boosting):")
print(gb_importance.sort_values(by='Importance', ascending=False).head(10))
