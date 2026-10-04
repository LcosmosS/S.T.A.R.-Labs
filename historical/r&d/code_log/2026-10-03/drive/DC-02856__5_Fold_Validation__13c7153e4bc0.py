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
# Load the dataset
df = pd.read_csv('SDSSDR19_200000.csv')
print(f"Dataset loaded with {df.shape[0]} rows and {df.shape[1]} columns.")


# Derive necessary features
# Compute colors
df['g_r'] = df['g'] - df['r']


# Approximate absolute magnitude (r-band) using redshift
# Distance modulus: DM = 5 * log10(d_L/10 pc), d_L ~ (c/H0) * z for small z
H0 = 70  # Hubble constant in km/s/Mpc
c = 3e5  # Speed of light in km/s
df['d_L'] = (c / H0) * df['redshift']  # Luminosity distance in Mpc
df['d_L'] = df['d_L'].replace(0, 1e-6)  # Avoid division by zero
df['dist_mod'] = 5 * np.log10(df['d_L'] * 1e6 / 10)  # Distance modulus
df['M_r'] = df['r'] - df['dist_mod']  # Absolute magnitude


# Estimate stellar mass (nsa_mstar) using a simplified color-magnitude relation
# log(M*) ~ -0.4 * (M_r - M_sun,r) + 0.4 * (g - r) + constant
M_sun_r = 4.64  # Absolute magnitude of the Sun in r-band
df['log_nsa_mstar'] = -0.4 * (df['M_r'] - M_sun_r) + 0.4 * df['g_r'] + 8.0  # Offset for scaling


# Estimate SFR using u-band magnitude as a proxy
df['log_SFR_Ha'] = -0.4 * df['u'] + 2.0  # Simplified proxy (adjust constant as needed)


# Estimate gas mass (log_Mass_gas) using SFR
df['log_Mass_gas'] = df['log_SFR_Ha'] + 8.0  # Simplified relation


# Approximate log_Mass (total mass) as log(nsa_mstar)
df['log_Mass'] = df['log_nsa_mstar']


# Approximate metallicity (OH_Mar13_N2_Re_fit) using mass-metallicity relation
df['OH_Mar13_N2_Re_fit'] = 8.9 - 0.5 * (df['log_nsa_mstar'] - 10)  # Simplified relation


# Approximate dust attenuation (Av_gas_Re) using g-r color
df['Av_gas_Re'] = 1.5 * df['g_r']  # Simplified proxy


# Define desired features
desired_features = [
    'log_Mass_gas', 'log_nsa_mstar', 'log_Mass', 'OH_Mar13_N2_Re_fit', 'Av_gas_Re'
]


# Since all desired features are derived, they should be available
available_features = [feat for feat in desired_features if feat in df.columns]
print(f"Using features: {available_features}")


# Handle missing values
df[available_features] = df[available_features].replace(-9999, np.nan)
imputer = SimpleImputer(strategy='median')
df[available_features] = imputer.fit_transform(df[available_features])


# Drop rows with missing target
df = df.dropna(subset=['log_SFR_Ha'])
y = df['log_SFR_Ha']
X = df[available_features]


# --- 2. Feature Engineering ---
# Generate polynomial features for interactions and nonlinear terms
poly = PolynomialFeatures(degree=2, include_bias=False, interaction_only=False)
X_poly = poly.fit_transform(X)
feature_names = poly.get_feature_names_out(available_features)
print(f"Generated {X_poly.shape[1]} polynomial features from {len(available_features)} base features.")


# --- 3. Data Splitting ---
X_train, X_test, y_train, y_test = train_test_split(X_poly, y, test_size=0.2, random_state=42)
print(f"Training set: {X_train.shape[0]} rows, Testing set: {X_test.shape[0]} rows")


# --- 4. Model Training with Hyperparameter Tuning ---
# Parameter grids for GridSearchCV
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


# Random Forest tuning
rf = RandomForestRegressor(random_state=42)
rf_grid = GridSearchCV(rf, rf_params, cv=5, scoring='neg_mean_squared_error', n_jobs=-1, verbose=2)
rf_grid.fit(X_train, y_train)
best_rf = rf_grid.best_estimator_
print(f"Best Random Forest hyperparameters: {rf_grid.best_params_}")


# Gradient Boosting tuning
gb = GradientBoostingRegressor(random_state=42, loss='huber')
gb_grid = GridSearchCV(gb, gb_params, cv=5, scoring='neg_mean_squared_error', n_jobs=-1, verbose=2)
gb_grid.fit(X_train, y_train)
best_gb = gb_grid.best_estimator_
print(f"Best Gradient Boosting hyperparameters: {gb_grid.best_params_}")


# --- 5. Model Evaluation ---
def evaluate_model(model, X_test, y_test, model_name):
    y_pred = model.predict(X_test)
    mse = mean_squared_error(y_test, y_pred)
    r2 = r2_score(y_test, y_pred)
    print(f"\n{model_name} Results:")
    print(f"Test MSE: {mse:.4f}, R-squared: {r2:.4f}")
    return y_pred


# Evaluate both models
y_pred_rf = evaluate_model(best_rf, X_test, y_test, "Random Forest")
y_pred_gb = evaluate_model(best_gb, X_test, y_test, "Gradient Boosting")


# --- 6. K-Fold Cross-Validation ---
kf = KFold(n_splits=5, shuffle=True, random_state=42)
rf_cv_mse = -cross_val_score(best_rf, X_poly, y, cv=kf, scoring='neg_mean_squared_error').mean()
rf_cv_r2 = cross_val_score(best_rf, X_poly, y, cv=kf, scoring='r2').mean()
print(f"\nRandom Forest K-Fold CV - Average MSE: {rf_cv_mse:.4f}, Average R-squared: {rf_cv_r2:.4f}")


gb_cv_mse = -cross_val_score(best_gb, X_poly, y, cv=kf, scoring='neg_mean_squared_error').mean()
gb_cv_r2 = cross_val_score(best_gb, X_poly, y, cv=kf, scoring='r2').mean()
print(f"Gradient Boosting K-Fold CV - Average MSE: {gb_cv_mse:.4f}, Average R-squared: {gb_cv_r2:.4f}")


# --- 7. Visualization ---
# Residual plot for Random Forest
plt.figure(figsize=(8, 6))
plt.scatter(y_pred_rf, y_test - y_pred_rf, alpha=0.5)
plt.axhline(0, color='red', linestyle='--')
plt.xlabel('Predicted log_SFR_Ha')
plt.ylabel('Residuals')
plt.title('Residuals vs. Predicted (Random Forest)')
plt.savefig('residuals_rf.png')
plt.close()


# Residual plot for Gradient Boosting
plt.figure(figsize=(8, 6))
plt.scatter(y_pred_gb, y_test - y_pred_gb, alpha=0.5)
plt.axhline(0, color='red', linestyle='--')
plt.xlabel('Predicted log_SFR_Ha')
plt.ylabel('Residuals')
plt.title('Residuals vs. Predicted (Gradient Boosting)')
plt.savefig('residuals_gb.png')
plt.close()


# --- 8. Feature Importance ---
rf_importance = pd.DataFrame({'Feature': feature_names, 'Importance': best_rf.feature_importances_})
print("\nTop 10 Important Features (Random Forest):")
print(rf_importance.sort_values(by='Importance', ascending=False).head(10))


gb_importance = pd.DataFrame({'Feature': feature_names, 'Importance': best_gb.feature_importances_})
print("\nTop 10 Important Features (Gradient Boosting):")
print(gb_importance.sort_values(by='Importance', ascending=False).head(10))


# --- Optional: Save Models ---
# joblib.dump(best_rf, 'best_rf_model.pkl')
# joblib.dump(best_gb, 'best_gb_model.pkl')
