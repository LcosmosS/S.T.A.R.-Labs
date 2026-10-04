import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import PolynomialFeatures
from sklearn.metrics import mean_squared_error, r2_score
import matplotlib.pyplot as plt


# Load the dataset
df = pd.read_csv('pipe3d_data2.csv')
print(f"Dataset loaded with {len(df)} rows and {len(df.columns)} columns.")


# Define target and base features
target = 'log_SFR_Ha'
base_features = ['log_Mass_gas', 'nsa_mstar', 'log_Mass', 'V-band_SB_at_Re', 'vel_sigma_Re', 'OH_Mar13_N2_Re_fit', 'Av_gas_Re']


# Impute missing values with median
imputer = SimpleImputer(strategy='median')
df[base_features] = imputer.fit_transform(df[base_features])


# Drop rows with missing target
df = df.dropna(subset=[target])
y = df[target]
X = df[base_features]


# Feature engineering: Create interactions and polynomials
df['log_Mass_gas_times_nsa_mstar'] = df['log_Mass_gas'] * df['nsa_mstar']
df['log_Mass_gas_times_metallicity'] = df['log_Mass_gas'] * df['OH_Mar13_N2_Re_fit']
df['log_Mass_gas_squared'] = df['log_Mass_gas'] ** 2
enhanced_features = base_features + ['log_Mass_gas_times_nsa_mstar', 'log_Mass_gas_times_metallicity', 'log_Mass_gas_squared']


# Use PolynomialFeatures for systematic generation (degree 2)
poly = PolynomialFeatures(degree=2, include_bias=False, interaction_only=False)
X_poly = poly.fit_transform(df[enhanced_features])
feature_names = poly.get_feature_names_out(enhanced_features)


# Split the data
X_train, X_test, y_train, y_test = train_test_split(X_poly, y, test_size=0.2, random_state=42)
print(f"Training set: {X_train.shape[0]} rows, Testing set: {X_test.shape[0]} rows")


# Train Random Forest with cross-validation
rf = RandomForestRegressor(random_state=42)
cv_scores = cross_val_score(rf, X_train, y_train, cv=5, scoring='neg_mean_squared_error')
print(f"Cross-validation MSE scores: {(-cv_scores).mean():.4f} (+/- {(-cv_scores).std() * 2:.4f})")


# Fit the model
rf.fit(X_train, y_train)


# Predict and evaluate
y_pred = rf.predict(X_test)
mse = mean_squared_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)
print(f"Test MSE: {mse:.4f}")
print(f"Test R-squared: {r2:.4f}")


# Feature importance
importances = rf.feature_importances_
importance_df = pd.DataFrame({'Feature': feature_names, 'Importance': importances})
importance_df = importance_df.sort_values(by='Importance', ascending=False)
print("\nTop 10 Important Features:")
print(importance_df.head(10))


# Plot predicted vs actual
plt.figure(figsize=(8,6))
plt.scatter(y_test, y_pred, alpha=0.5)
plt.plot([y_test.min(), y_test.max()], [y_test.min(), y_test.max()], 'r--')
plt.xlabel('Actual log_SFR_Ha')
plt.ylabel('Predicted log_SFR_Ha')
plt.title('Predicted vs Actual log_SFR_Ha')
plt.savefig('predicted_vs_actual.png')
plt.close()


# Plot residuals
residuals = y_test - y_pred
plt.figure(figsize=(8,6))
plt.scatter(y_pred, residuals, alpha=0.5)
plt.axhline(0, color='r', linestyle='--')
plt.xlabel('Predicted log_SFR_Ha')
plt.ylabel('Residuals')
plt.title('Residuals vs Predicted')
plt.savefig('residuals.png')
plt.close()


# Plot histogram of residuals
plt.figure(figsize=(8,6))
plt.hist(residuals, bins=30, edgecolor='black')
plt.xlabel('Residuals')
plt.ylabel('Frequency')
plt.title('Histogram of Residuals')
plt.savefig('residuals_histogram.png')
plt.close()
