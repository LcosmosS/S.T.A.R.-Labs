import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split, RandomizedSearchCV
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import mean_squared_error
import shap
from sklearn.impute import SimpleImputer
from scipy.stats import randint
from sklearn.neighbors import NearestNeighbors
from sklearn.neighbors import KernelDensity
import matplotlib.pyplot as plt
from numpy.polynomial.polynomial import Polynomial

# Step 1: Load the merged dataset
df1 = pd.read_csv('merged_output.csv', low_memory=False)

# Print columns to confirm
print("Columns in merged DataFrame:", df1.columns)

# --- Check for 'fS' flux column and calculate SFR ---
flux_columns = [col for col in df1.columns if 'fS' in col]
print(f"Found flux columns: {flux_columns}")

# If we find any flux columns, we can use the first one found for SFR calculation
if flux_columns:
    flux_col = flux_columns[0]  # Take the first one found
    df1['SFR'] = df1[flux_col] / (1.26e-41)  # SFR in solar masses per year
    print(f"SFR column successfully created from {flux_col}.")
else:
    print("No 'fS' column found. Cannot calculate SFR.")

# --- Check for necessary columns and handle suffixes ---
if 'RAJ2000' in df1.columns:
    df1.rename(columns={'RAJ2000': 'ra'}, inplace=True)
if 'DEJ2000' in df1.columns:
    df1.rename(columns={'DEJ2000': 'dec'}, inplace=True)
if 'z' in df1.columns:
    df1.rename(columns={'z': 'redshift'}, inplace=True)

# After renaming, check if the required columns are available
print(f"Columns after renaming: {df1.columns}")

# Ensure 'SFR' is available as the target (we just calculated it above)
if 'SFR' in df1.columns:
    # Step 2: Impute missing values with the mean or median
    imputer = SimpleImputer(strategy='mean')  # You can change to 'median' if desired
    
    # Impute missing values in all numerical columns
    df1[['ra', 'dec', 'redshift', 'SFR']] = imputer.fit_transform(df1[['ra', 'dec', 'redshift', 'SFR']])

    X = df1[['ra', 'dec', 'redshift']]  # Use available features: ra, dec, and redshift
    y = df1['SFR']  # Target: 'SFR' (Star Formation Rate)
else:
    print("SFR column not available for target variable.")
    X = df1[['ra', 'dec', 'redshift']]  # Use available features if SFR is missing
    y = df1['SFR']  # Use SFR if available, otherwise fallback to a proxy or other method

# Step 5: Split data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Step 6: Standardize the features (optional but often helpful for gradient-based models)
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# --- Nearest Neighbor Calculation ---
# Use nearest neighbors to calculate local density estimates
nearest_neighbors = NearestNeighbors(n_neighbors=10, algorithm='ball_tree')
nearest_neighbors.fit(X_train_scaled)
distances, indices = nearest_neighbors.kneighbors(X_train_scaled)

# --- KDE with Gaussian Kernel for Local Density Estimation ---
# Apply Kernel Density Estimation (KDE) with a Gaussian kernel
kde = KernelDensity(kernel='gaussian', bandwidth=0.5)  # You can adjust the bandwidth
kde.fit(X_train_scaled)

# Score_samples returns the log of the estimated density
log_densities = kde.score_samples(X_test_scaled)

# Convert log densities to actual densities
densities = np.exp(log_densities)

# --- Polynomial Curve Fitting ---
# Fit a polynomial of degree 3 to the KDE density estimates for smoother modeling
degree = 3
polynomial_coefficients = np.polyfit(X_test_scaled[:, 0], densities, degree)  # Fitting to 'ra' feature for simplicity

# Create a polynomial function from the coefficients
poly_func = np.poly1d(polynomial_coefficients)

# Plot the polynomial fit over the KDE
x_range = np.linspace(X_test_scaled[:, 0].min(), X_test_scaled[:, 0].max(), 100)
y_range = poly_func(x_range)

plt.figure(figsize=(10, 6))
plt.plot(x_range, y_range, label='Polynomial Fit', color='red')
plt.scatter(X_test_scaled[:, 0], densities, label='KDE Density', color='blue', alpha=0.5)
plt.xlabel('ra (Right Ascension)')
plt.ylabel('Density')
plt.legend()
plt.show()

# --- Derivative Calculation of the Polynomial Function ---
# Compute the derivative of the fitted polynomial
derivative_func = poly_func.deriv()

# Evaluate the derivative at various points
derivative_values = derivative_func(x_range)

# Plot the derivative
plt.figure(figsize=(10, 6))
plt.plot(x_range, derivative_values, label='Polynomial Derivative', color='green')
plt.xlabel('ra (Right Ascension)')
plt.ylabel('Derivative of Density')
plt.legend()
plt.show()

# Step 7: Train the Random Forest model using Randomized Search
rf_param_dist = {
    'n_estimators': randint(100, 1000),
    'max_depth': randint(10, 100),
    'min_samples_split': randint(2, 20),
    'min_samples_leaf': randint(1, 20),
    'max_features': ['sqrt', 'log2', None]  # Replaced 'auto' with 'sqrt' and 'log2'
}

rf_random_search = RandomizedSearchCV(
    RandomForestRegressor(random_state=42),
    param_distributions=rf_param_dist,
    n_iter=10,  # Number of random combinations to try
    cv=3,  # Cross-validation
    random_state=42,
    n_jobs=-1  # Use all available cores
)

rf_random_search.fit(X_train_scaled, y_train)
best_rf_model = rf_random_search.best_estimator_

# Step 8: Train the Gradient Boosting model using Randomized Search
gb_param_dist = {
    'n_estimators': randint(100, 1000),
    'learning_rate': [0.001, 0.01, 0.1, 0.2, 0.3],
    'max_depth': randint(3, 20),
    'min_samples_split': randint(2, 20),
    'min_samples_leaf': randint(1, 20),
}

gb_random_search = RandomizedSearchCV(
    GradientBoostingRegressor(random_state=42),
    param_distributions=gb_param_dist,
    n_iter=10,  # Number of random combinations to try
    cv=3,  # Cross-validation
    random_state=42,
    n_jobs=-1  # Use all available cores
)

gb_random_search.fit(X_train_scaled, y_train)
best_gb_model = gb_random_search.best_estimator_

# Step 9: Evaluate both models' performance
y_pred_rf = best_rf_model.predict(X_test_scaled)
mse_rf = mean_squared_error(y_test, y_pred_rf)
r2_rf = best_rf_model.score(X_test_scaled, y_test)

y_pred_gb = best_gb_model.predict(X_test_scaled)
mse_gb = mean_squared_error(y_test, y_pred_gb)
r2_gb = best_gb_model.score(X_test_scaled, y_test)

print(f"Random Forest - Mean Squared Error: {mse_rf}, R²: {r2_rf}")
print(f"Gradient Boosting - Mean Squared Error: {mse_gb}, R²: {r2_gb}")

# --- SHAP Analysis ---
# Use SHAP for both models

# For Random Forest
explainer_rf = shap.TreeExplainer(best_rf_model)
shap_values_rf = explainer_rf.shap_values(X_test_scaled)

# For Gradient Boosting
explainer_gb = shap.TreeExplainer(best_gb_model)
shap_values_gb = explainer_gb.shap_values(X_test_scaled)

# Plot SHAP summary for Random Forest
shap.summary_plot(shap_values_rf, X_test)

# Plot SHAP summary for Gradient Boosting
shap.summary_plot(shap_values_gb, X_test)

# Optional: Save the merged data with SFR if needed
df1.to_csv('merged_output_with_SFR.csv', index=False)

# Print the first few rows to verify the merged data
print(df1.head())
