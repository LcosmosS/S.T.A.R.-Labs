import pandas as pd
import numpy as np
from sklearn.ensemble import GradientBoostingRegressor, RandomForestRegressor
from sklearn.model_selection import train_test_split, RandomizedSearchCV, KFold, cross_val_score
from sklearn.metrics import mean_squared_error, r2_score
import matplotlib.pyplot as plt
import joblib

# --- 1. Data Preparation ---
# Load dataset
df = pd.read_csv('compiled_sfr_dataset.csv')
print(f"Dataset loaded with {df.shape[0]} rows and {df.shape[1]} columns.")

# Define target and features (adjust these column names as per your dataset)
target = 'log_SFR_Ha'
features = ['log_Mass_gas', 'nsa_mstar', 'log_Mass', 'vel_sigma_Re', 
            'OH_Mar13_N2_Re_fit', 'Av_gas_Re', 'zcomp_1Mpc', 'LOGMSTARS', 'SFR_PETRORAD_R']
X = df[features]
y = df[target]

# Handle missing values by dropping rows with NaNs
X = X.dropna()
y = y.loc[X.index]  # Align y with X after dropping rows

# --- 2. Outlier Detection ---
# Identify outliers in the target variable using IQR
Q1, Q3 = y.quantile(0.25), y.quantile(0.75)
IQR = Q3 - Q1
outliers = (y < Q1 - 1.5 * IQR) | (y > Q3 + 1.5 * IQR)
print(f"Number of outliers in target: {outliers.sum()}")

# --- 3. Data Splitting ---
# Split data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
print(f"Training set: {X_train.shape[0]} rows, Testing set: {X_test.shape[0]} rows")

# Subset outliers for the test set
outliers_test = outliers.loc[y_test.index]

# --- 4. Model Training with Hyperparameter Tuning ---
# Define parameter grids for RandomizedSearchCV
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

# RandomizedSearchCV for Random Forest
rf = RandomForestRegressor(random_state=42)
rf_random = RandomizedSearchCV(rf, rf_params, n_iter=10, cv=3, scoring='neg_mean_squared_error', n_jobs=-1, verbose=2)
rf_random.fit(X_train, y_train)
best_rf = rf_random.best_estimator_
print(f"Best RF hyperparameters: {rf_random.best_params_}")

# RandomizedSearchCV for Gradient Boosting
gb = GradientBoostingRegressor(random_state=42, loss='huber')
gb_random = RandomizedSearchCV(gb, gb_params, n_iter=10, cv=3, scoring='neg_mean_squared_error', n_jobs=-1, verbose=2)
gb_random.fit(X_train, y_train)
best_gb = gb_random.best_estimator_
print(f"Best GB hyperparameters: {gb_random.best_params_}")

# --- 5. Model Evaluation ---
def evaluate_model(model, X_test, y_test, outliers_test):
    """Evaluate model performance on full test set, outliers, and non-outliers."""
    y_pred = model.predict(X_test)
    mse_full = mean_squared_error(y_test, y_pred)
    r2_full = r2_score(y_test, y_pred)
    if outliers_test.sum() > 0:
        mse_outliers = mean_squared_error(y_test[outliers_test], y_pred[outliers_test])
        r2_outliers = r2_score(y_test[outliers_test], y_pred[outliers_test])
    else:
        mse_outliers = np.nan
        r2_outliers = np.nan
    mse_non_outliers = mean_squared_error(y_test[~outliers_test], y_pred[~outliers_test])
    r2_non_outliers = r2_score(y_test[~outliers_test], y_pred[~outliers_test])
    return mse_full, r2_full, mse_outliers, r2_outliers, mse_non_outliers, r2_non_outliers

# Evaluate Random Forest
rf_results = evaluate_model(best_rf, X_test, y_test, outliers_test)
print("\nRandom Forest Results:")
print(f"Full Test Set - MSE: {rf_results[0]:.4f}, R-squared: {rf_results[1]:.4f}")
print(f"Outliers - MSE: {rf_results[2]:.4f}, R-squared: {rf_results[3]:.4f}")
print(f"Non-Outliers - MSE: {rf_results[4]:.4f}, R-squared: {rf_results[5]:.4f}")

# Evaluate Gradient Boosting
gb_results = evaluate_model(best_gb, X_test, y_test, outliers_test)
print("\nGradient Boosting Results:")
print(f"Full Test Set - MSE: {gb_results[0]:.4f}, R-squared: {gb_results[1]:.4f}")
print(f"Outliers - MSE: {gb_results[2]:.4f}, R-squared: {gb_results[3]:.4f}")
print(f"Non-Outliers - MSE: {gb_results[4]:.4f}, R-squared: {gb_results[5]:.4f}")

# --- 6. K-Fold Cross-Validation ---
kf = KFold(n_splits=5, shuffle=True, random_state=42)

# Random Forest cross-validation
rf_cv_mse = -cross_val_score(best_rf, X, y, cv=kf, scoring='neg_mean_squared_error').mean()
rf_cv_r2 = cross_val_score(best_rf, X, y, cv=kf, scoring='r2').mean()
print(f"\nRandom Forest K-Fold CV - Average MSE: {rf_cv_mse:.4f}, Average R-squared: {rf_cv_r2:.4f}")

# Gradient Boosting cross-validation
gb_cv_mse = -cross_val_score(best_gb, X, y, cv=kf, scoring='neg_mean_squared_error').mean()
gb_cv_r2 = cross_val_score(best_gb, X, y, cv=kf, scoring='r2').mean()
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
rf_importance = pd.DataFrame({'Feature': features, 'Importance': best_rf.feature_importances_})
print("\nTop 10 Important Features (Random Forest):")
print(rf_importance.sort_values(by='Importance', ascending=False).head(10))

# Gradient Boosting feature importance
gb_importance = pd.DataFrame({'Feature': features, 'Importance': best_gb.feature_importances_})
print("\nTop 10 Important Features (Gradient Boosting):")
print(gb_importance.sort_values(by='Importance', ascending=False).head(10))

# --- Optional: Save Models ---
# Uncomment the lines below to save the trained models
# joblib.dump(best_rf, 'best_rf_model.pkl')
# joblib.dump(best_gb, 'best_gb_model.pkl')