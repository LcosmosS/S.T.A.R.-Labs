import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.model_selection import KFold, cross_val_score, GridSearchCV, train_test_split
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.metrics import mean_squared_error, r2_score
import joblib
import xgboost as xgb

# Step 1: Load the dataset
# Replace 'filtered_Pipe3D.csv' with your actual dataset file path
df = pd.read_csv('filtered_Pipe3D.csv')
print(f"Dataset loaded with {len(df)} rows and {len(df.columns)} columns.")

# Step 2: Define features (X) and target (y)
# Replace 'log_SFR_Ha' with your actual target column name
X = df.drop(columns=['log_SFR_Ha'])  # Features
y = df['log_SFR_Ha']                 # Target

# Step 3: Split the data into training and testing sets (80% train, 20% test)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
print(f"Training set: {X_train.shape[0]} rows, Testing set: {X_test.shape[0]} rows")

# Step 4: Set up 5-fold cross-validation
kf = KFold(n_splits=5, shuffle=True, random_state=42)

# Step 5: Initialize the Random Forest model
rf_model = RandomForestRegressor(random_state=42)

# Step 6: Perform cross-validation and calculate MSE for each fold
mse_scores = cross_val_score(rf_model, X_train, y_train, cv=kf, scoring='neg_mean_squared_error')
mse_scores = -mse_scores  # Convert to positive MSE
print(f"MSE for each fold: {mse_scores}")
print(f"Average MSE from cross-validation: {np.mean(mse_scores):.4f}")

# Step 7: Define a grid of hyperparameters for tuning
param_grid = {
    'n_estimators': [100, 200, 300],
    'max_depth': [10, 20, None],
    'min_samples_split': [2, 5, 10]
}

# Step 8: Perform hyperparameter tuning with GridSearchCV
grid_search = GridSearchCV(estimator=RandomForestRegressor(random_state=42),
                           param_grid=param_grid,
                           cv=5,
                           scoring='neg_mean_squared_error',
                           n_jobs=-1)
grid_search.fit(X_train, y_train)

# Get the best hyperparameters and model
best_params = grid_search.best_params_
best_rf_model = grid_search.best_estimator_
print(f"Best hyperparameters: {best_params}")

# Step 9: Train the best Random Forest model on the full training set
best_rf_model.fit(X_train, y_train)

# Step 10: Make predictions on the test set
y_pred_rf = best_rf_model.predict(X_test)

# Step 11: Evaluate the tuned Random Forest model on the test set
mse_rf = mean_squared_error(y_test, y_pred_rf)
r2_rf = r2_score(y_test, y_pred_rf)
print(f"Random Forest Tuned Mean Squared Error (MSE): {mse_rf:.4f}")
print(f"Random Forest Tuned R-squared: {r2_rf:.4f}")

# Step 12: Save the best Random Forest model
joblib.dump(best_rf_model, 'best_rf_model.pkl')
print("Best Random Forest model saved to 'best_rf_model.pkl'")

# Step 13: Extract and Display Feature Importances
importances = best_rf_model.feature_importances_
feature_names = X_train.columns
feature_importance_df = pd.DataFrame({'Feature': feature_names, 'Importance': importances})
feature_importance_df = feature_importance_df.sort_values(by='Importance', ascending=False)
print("\nTop 5 Most Important Features:")
print(feature_importance_df.head())

# Plot feature importances
plt.figure(figsize=(10, 6))
plt.barh(feature_importance_df['Feature'], feature_importance_df['Importance'], color='skyblue')
plt.xlabel('Importance')
plt.ylabel('Feature')
plt.title('Feature Importances from Random Forest')
plt.gca().invert_yaxis()  # Most important feature at the top
plt.savefig('feature_importances.png')
plt.show()

# Step 14: Residual Analysis
residuals_rf = y_test - y_pred_rf

# Plot predicted vs. actual values
plt.figure(figsize=(8, 6))
plt.scatter(y_test, y_pred_rf, alpha=0.5)
plt.plot([min(y_test), max(y_test)], [min(y_test), max(y_test)], 'r--')  # 45-degree line
plt.xlabel('Actual SFR')
plt.ylabel('Predicted SFR')
plt.title('Predicted vs. Actual Star Formation Rates (Random Forest)')
plt.savefig('predicted_vs_actual_rf.png')
plt.show()

# Plot histogram of residuals
plt.figure(figsize=(8, 6))
plt.hist(residuals_rf, bins=30, edgecolor='black')
plt.xlabel('Residuals (Actual - Predicted)')
plt.ylabel('Frequency')
plt.title('Histogram of Residuals (Random Forest)')
plt.savefig('residuals_histogram_rf.png')
plt.show()

# Plot residuals vs. predicted values
plt.figure(figsize=(8, 6))
plt.scatter(y_pred_rf, residuals_rf, alpha=0.5)
plt.axhline(y=0, color='red', linestyle='--')
plt.xlabel('Predicted Values')
plt.ylabel('Residuals (Actual - Predicted)')
plt.title('Residuals vs. Predicted Values (Random Forest)')
plt.savefig('residuals_vs_predicted_rf.png')
plt.show()

# Step 15: Model Comparison - Gradient Boosting
gb_model = GradientBoostingRegressor(random_state=42)
gb_model.fit(X_train, y_train)
y_pred_gb = gb_model.predict(X_test)
mse_gb = mean_squared_error(y_test, y_pred_gb)
r2_gb = r2_score(y_test, y_pred_gb)
print(f"\nGradient Boosting MSE: {mse_gb:.4f}")
print(f"Gradient Boosting R-squared: {r2_gb:.4f}")

# Step 16: Model Comparison - XGBoost
xgb_model = xgb.XGBRegressor(random_state=42)
xgb_model.fit(X_train, y_train)
y_pred_xgb = xgb_model.predict(X_test)
mse_xgb = mean_squared_error(y_test, y_pred_xgb)
r2_xgb = r2_score(y_test, y_pred_xgb)
print(f"\nXGBoost MSE: {mse_xgb:.4f}")
print(f"XGBoost R-squared: {r2_xgb:.4f}")

# Step 17: Summarize Model Performance
print("\nModel Performance Summary:")
print(f"Random Forest - MSE: {mse_rf:.4f}, R-squared: {r2_rf:.4f}")
print(f"Gradient Boosting - MSE: {mse_gb:.4f}, R-squared: {r2_gb:.4f}")
print(f"XGBoost - MSE: {mse_xgb:.4f}, R-squared: {r2_xgb:.4f}")