import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.model_selection import train_test_split, GridSearchCV, KFold, cross_val_score
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import PolynomialFeatures
from sklearn.metrics import mean_squared_error, r2_score
import matplotlib.pyplot as plt
import joblib


# --- 1. Data Preparation ---
# Load dataset
df = pd.read_csv('pipe3d_data2.csv')
print(f"Dataset loaded with {df.shape[0]} rows and {df.shape[1]} columns.")


# Define target and base features
target = 'log_SFR_Ha'
base_features = ['log_Mass_gas', 'nsa_mstar', 'log_Mass', 'vel_sigma_Re', 
                 'OH_Mar13_N2_Re_fit', 'Av_gas_Re', 'zcomp_1Mpc', 'LOGMSTARS', 'SFR_PETRORAD_R']


# Additional features to consider
additional_features = ['Age_LW_Re_fit', 'vel_disp_ssp_1Re', 'L-dust', 'sSfr_0_1Gr', 
                       'mass_dust', 'tau_v', 'mass_stellar']


# Combine base and additional features
all_features = base_features + additional_features


# Handle missing values: replace sentinel values and impute
df[all_features] = df[all_features].replace(-9999, np.nan)
imputer = SimpleImputer(strategy='median')
df[all_features] = imputer.fit_transform(df[all_features])


# Quality control: filter for valid data using QCFLAG
if 'QCFLAG' in df.columns:
    df = df[df['QCFLAG'] == 1]
    print(f"Dataset filtered with QCFLAG == 1: {df.shape[0]} rows remaining.")


# Drop rows with missing target
df = df.dropna(subset=[target])
y = df[target]
X = df[all_features]


# --- 2. Feature Engineering ---
# Create interaction and polynomial terms
poly = PolynomialFeatures(degree=2, include_bias=False, interaction_only=False)
X_poly = poly.fit_transform(X)
feature_names = poly.get_feature_names_out(all_features)


# Add specific interaction terms
df['log_Mass_gas_times_nsa_mstar'] = df['log_Mass_gas'] * df['nsa_mstar']
df['log_Mass_gas_times_OH'] = df['log_Mass_gas'] * df['OH_Mar13_N2_Re_fit']
df['log_Mass_gas_squared'] = df['log_Mass_gas'] ** 2


# Update feature list with new terms
enhanced_features = all_features + ['log_Mass_gas_times_nsa_mstar', 'log_Mass_gas_times_OH', 'log_Mass_gas_squared']


# Use PolynomialFeatures for systematic generation
X_poly = poly.fit_transform(df[enhanced_features])
feature_names = poly.get_feature_names_out(enhanced_features)


# --- 3. Data Splitting ---
# Split data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X_poly, y, test_size=0.2, random_state=42)
print(f"Training set: {X_train.shape[0]} rows, Testing set: {X_test.shape[0]} rows")


# --- 4. Model Training with Hyperparameter Tuning ---
# Define parameter grids for GridSearchCV
rf_params = {
    'n_estimators': [100, 200, 300],
    'max_depth': [10, 20, None],
    'min_samples_split': [2, 5, 10]
}


gb_params = {
    'learning_rate': [0.01, 0.05, 0.1],
    'max_depth': [3, 5, 7],
    'n_estimators': [100, 200, 300]
}


# GridSearchCV for Random Forest
rf = RandomForestRegressor(random_state=42)
rf_grid = GridSearchCV(rf, rf_params, cv=3, scoring='neg_mean_squared_error', n_jobs=-1, verbose=2)
rf_grid.fit(X_train, y_train)
best_rf = rf_grid.best_estimator_
print(f"Best RF hyperparameters: {rf_grid.best_params_}")


# GridSearchCV for Gradient Boosting
gb = GradientBoostingRegressor(random_state=42, loss='huber')
gb_grid = GridSearchCV(gb, gb_params, cv=3, scoring='neg_mean_squared_error', n_jobs=-1, verbose=2)
gb_grid.fit(X_train, y_train)
best_gb = gb_grid.best_estimator_
print(f"Best GB hyperparameters: {gb_grid.best_params_}")


# --- 5. Model Evaluation ---
def evaluate_model(model, X_test, y_test):
    """Evaluate model performance on the test set."""
    y_pred = model.predict(X_test)
    mse = mean_squared_error(y_test, y_pred)
    r2 = r2_score(y_test, y_pred)
    return mse, r2


# Evaluate Random Forest
rf_mse, rf_r2 = evaluate_model(best_rf, X_test, y_test)
print("\nRandom Forest Results:")
print(f"Test MSE: {rf_mse:.4f}, R-squared: {rf_r2:.4f}")


# Evaluate Gradient Boosting
gb_mse, gb_r2 = evaluate_model(best_gb, X_test, y_test)
print("\nGradient Boosting Results:")
print(f"Test MSE: {gb_mse:.4f}, R-squared: {gb_r2:.4f}")


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
# Random Forest feature importance
rf_importance = pd.DataFrame({'Feature': feature_names, 'Importance': best_rf.feature_importances_})
print("\nTop 10 Important Features (Random Forest):")
print(rf_importance.sort_values(by='Importance', ascending=False).head(10))


# Gradient Boosting feature importance
gb_importance = pd.DataFrame({'Feature': feature_names, 'Importance': best_gb.feature_importances_})
print("\nTop 10 Important Features (Gradient Boosting):")
print(gb_importance.sort_values(by='Importance', ascending=False).head(10))


# --- Optional: Save Models ---
# Uncomment the lines below to save the trained models
# joblib.dump(best_rf, 'best_rf_model.pkl')
# joblib.dump(best_gb, 'best_gb_model.pkl')
