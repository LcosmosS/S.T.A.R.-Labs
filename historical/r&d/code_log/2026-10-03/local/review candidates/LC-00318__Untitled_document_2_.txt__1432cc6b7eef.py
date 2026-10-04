import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.preprocessing import PolynomialFeatures
from sklearn.metrics import mean_squared_error, r2_score
import matplotlib.pyplot as plt


# Load the filtered dataset
df = pd.read_csv('filtered_pipe3d_data.csv')  # Ensure this has OH_Mar13_N2_Re_fit and Av_gas_Re
print(f"Dataset loaded with {len(df)} rows and {len(df.columns)} columns.")


# Define features, including new ones for testing
base_features = ['log_Mass_gas', 'nsa_mstar', 'log_Mass', 'V-band_SB_at_Re', 'vel_sigma_Re']
new_features = ['OH_Mar13_N2_Re_fit', 'Av_gas_Re']
all_features = base_features + new_features


# Handle missing values with mean imputation
df[all_features] = df[all_features].fillna(df[all_features].mean())


# Feature engineering: Create interactions and polynomials
df['log_Mass_gas_times_nsa_mstar'] = df['log_Mass_gas'] * df['nsa_mstar']
df['log_Mass_gas_times_OH'] = df['log_Mass_gas'] * df['OH_Mar13_N2_Re_fit']
df['log_Mass_gas_squared'] = df['log_Mass_gas'] ** 2


# Use PolynomialFeatures for systematic generation
poly = PolynomialFeatures(degree=2, interaction_only=False, include_bias=False)
X = df[all_features]
X_poly = poly.fit_transform(X)
feature_names = poly.get_feature_names_out(all_features)
df_poly = pd.DataFrame(X_poly, columns=feature_names)


# Define target
y = df['log_SFR_Ha']


# Split the data
X_train, X_test, y_train, y_test = train_test_split(df_poly, y, test_size=0.2, random_state=42)
print(f"Training set: {X_train.shape[0]} rows, Testing set: {X_test.shape[0]} rows")


# Train and tune Random Forest
rf_param_grid = {'n_estimators': [100, 200, 300], 'max_depth': [10, 20, None], 'min_samples_split': [2, 5, 10]}
rf_grid = GridSearchCV(RandomForestRegressor(random_state=42), rf_param_grid, cv=5, scoring='neg_mean_squared_error', n_jobs=-1)
rf_grid.fit(X_train, y_train)
best_rf = rf_grid.best_estimator_
print(f"Best RF hyperparameters: {rf_grid.best_params_}")


# Train and tune Gradient Boosting
gb_param_grid = {'learning_rate': [0.01, 0.05, 0.1], 'max_depth': [3, 5, 7], 'n_estimators': [100, 200, 300]}
gb_grid = GridSearchCV(GradientBoostingRegressor(random_state=42), gb_param_grid, cv=5, scoring='neg_mean_squared_error', n_jobs=-1)
gb_grid.fit(X_train, y_train)
best_gb = gb_grid.best_estimator_
print(f"Best GB hyperparameters: {gb_grid.best_params_}")


# Evaluate both models
for model, name in [(best_rf, 'Random Forest'), (best_gb, 'Gradient Boosting')]:
    y_pred = model.predict(X_test)
    mse = mean_squared_error(y_test, y_pred)
    r2 = r2_score(y_test, y_pred)
    print(f"\n{name} - MSE: {mse:.4f}, R-squared: {r2:.4f}")


    # Feature importance for the model
    importances = model.feature_importances_
    importance_df = pd.DataFrame({'Feature': feature_names, 'Importance': importances})
    importance_df = importance_df.sort_values(by='Importance', ascending=False)
    print(f"\nTop 5 features for {name}:")
    print(importance_df.head())


    # Residual plot
    residuals = y_test - y_pred
    plt.figure(figsize=(8, 6))
    plt.scatter(y_pred, residuals, alpha=0.5)
    plt.axhline(y=0, color='red', linestyle='--')
    plt.xlabel('Predicted SFR')
    plt.ylabel('Residuals')
    plt.title(f'Residuals vs. Predicted SFR ({name})')
    plt.savefig(f'residuals_{name.lower().replace(" ", "_")}.png')
    plt.close()  # Close to avoid display in non-interactive environment


    # Histogram of residuals
    plt.figure(figsize=(8, 6))
    plt.hist(residuals, bins=30, edgecolor='black')
    plt.xlabel('Residuals')
    plt.ylabel('Frequency')
    plt.title(f'Histogram of Residuals ({name})')
    plt.savefig(f'residuals_histogram_{name.lower().replace(" ", "_")}.png')
    plt.close()  # Close to avoid display in non-interactive environment
