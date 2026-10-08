import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.model_selection import KFold, cross_val_score, train_test_split
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import PolynomialFeatures
from sklearn.metrics import mean_squared_error, r2_score

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

# --- 3. K-Fold Cross-Validation Setup ---
# Define k-fold cross-validation with 5 folds
kf = KFold(n_splits=5, shuffle=True, random_state=42)

# Initialize models
rf = RandomForestRegressor(n_estimators=200, max_depth=10, min_samples_split=10, random_state=42)
gb = GradientBoostingRegressor(learning_rate=0.05, max_depth=7, n_estimators=100, loss='huber', random_state=42)

# --- 4. Cross-Validation for Random Forest ---
rf_mse_scores = cross_val_score(rf, X_poly, y, cv=kf, scoring='neg_mean_squared_error')
rf_mse_avg = -rf_mse_scores.mean()
rf_mse_std = rf_mse_scores.std()

rf_r2_scores = cross_val_score(rf, X_poly, y, cv=kf, scoring='r2')
rf_r2_avg = rf_r2_scores.mean()
rf_r2_std = rf_r2_scores.std()

print("\nRandom Forest Cross-Validation Results:")
print(f"Average MSE: {rf_mse_avg:.4f} (+/- {rf_mse_std:.4f})")
print(f"Average R-squared: {rf_r2_avg:.4f} (+/- {rf_r2_std:.4f})")

# --- 5. Cross-Validation for Gradient Boosting ---
gb_mse_scores = cross_val_score(gb, X_poly, y, cv=kf, scoring='neg_mean_squared_error')
gb_mse_avg = -gb_mse_scores.mean()
gb_mse_std = gb_mse_scores.std()

gb_r2_scores = cross_val_score(gb, X_poly, y, cv=kf, scoring='r2')
gb_r2_avg = gb_r2_scores.mean()
gb_r2_std = gb_r2_scores.std()

print("\nGradient Boosting Cross-Validation Results:")
print(f"Average MSE: {gb_mse_avg:.4f} (+/- {gb_mse_std:.4f})")
print(f"Average R-squared: {gb_r2_avg:.4f} (+/- {gb_r2_std:.4f})")

# --- 6. Final Evaluation on Test Set ---
X_train, X_test, y_train, y_test = train_test_split(X_poly, y, test_size=0.2, random_state=42)

# Random Forest
rf.fit(X_train, y_train)
y_pred_rf = rf.predict(X_test)
mse_rf = mean_squared_error(y_test, y_pred_rf)
r2_rf = r2_score(y_test, y_pred_rf)
print(f"\nRandom Forest Test Set - MSE: {mse_rf:.4f}, R-squared: {r2_rf:.4f}")

# Gradient Boosting
gb.fit(X_train, y_train)
y_pred_gb = gb.predict(X_test)
mse_gb = mean_squared_error(y_test, y_pred_gb)
r2_gb = r2_score(y_test, y_pred_gb)
print(f"Gradient Boosting Test Set - MSE: {mse_gb:.4f}, R-squared: {r2_gb:.4f}")