import pandas as pd
import numpy as np
from sklearn.ensemble import GradientBoostingRegressor
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

# Apply PolynomialFeatures for degree 2 to include interactions and squares
poly = PolynomialFeatures(degree=2, include_bias=False)
X_poly = poly.fit_transform(X)
feature_names = poly.get_feature_names_out(base_features)

# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X_poly, y, test_size=0.2, random_state=42)
print(f"Training set: {X_train.shape[0]} rows, Testing set: {X_test.shape[0]} rows")

# Initialize and train Gradient Boosting Regressor
gb = GradientBoostingRegressor(n_estimators=100, learning_rate=0.1, max_depth=3, random_state=42)

# Perform cross-validation
cv_scores = cross_val_score(gb, X_train, y_train, cv=5, scoring='neg_mean_squared_error')
print(f"Cross-validation MSE: {(-cv_scores).mean():.4f} (+/- {(-cv_scores).std() * 2:.4f})")

# Fit the model on the entire training set
gb.fit(X_train, y_train)

# Predict on the test set
y_pred = gb.predict(X_test)

# Calculate evaluation metrics
mse = mean_squared_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)
print(f"Test MSE: {mse:.4f}")
print(f"Test R-squared: {r2:.4f}")

# Feature importances
importances = gb.feature_importances_
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
plt.savefig('predicted_vs_actual_gb.png')
plt.close()

# Plot residuals vs predicted
residuals = y_test - y_pred
plt.figure(figsize=(8,6))
plt.scatter(y_pred, residuals, alpha=0.5)
plt.axhline(0, color='r', linestyle='--')
plt.xlabel('Predicted log_SFR_Ha')
plt.ylabel('Residuals')
plt.title('Residuals vs Predicted')
plt.savefig('residuals_gb.png')
plt.close()

# Plot histogram of residuals
plt.figure(figsize=(8,6))
plt.hist(residuals, bins=30, edgecolor='black')
plt.xlabel('Residuals')
plt.ylabel('Frequency')
plt.title('Histogram of Residuals')
plt.savefig('residuals_histogram_gb.png')
plt.close()
