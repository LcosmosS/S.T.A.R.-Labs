import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.model_selection import KFold, cross_val_score, GridSearchCV, train_test_split
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.metrics import mean_squared_error, r2_score
import joblib
import xgboost as xgb


# Step 1: Load the dataset
df = pd.read_csv('filtered_Pipe3D.csv')  # Replace with your dataset file
print(f"Dataset loaded with {len(df)} rows and {len(df.columns)} columns.")


# Step 2: Feature Engineering - Add interaction term
# Interaction between log_Mass_gas and log_Mass to capture combined effects
if 'log_Mass_gas' in df.columns and 'log_Mass' in df.columns:
    df['log_Mass_gas_times_log_Mass'] = df['log_Mass_gas'] * df['log_Mass']
    print("Added interaction term: log_Mass_gas_times_log_Mass")


# Step 3: Define features (X) and target (y)
X = df.drop(columns=['log_SFR_Ha'])  # Replace 'log_SFR_Ha' with your target column
y = df['log_SFR_Ha']


# Step 4: Split the data into training and testing sets (80% train, 20% test)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
print(f"Training set: {X_train.shape[0]} rows, Testing set: {X_test.shape[0]} rows")


# Step 5: Set up 5-fold cross-validation
kf = KFold(n_splits=5, shuffle=True, random_state=42)


# Step 6: Initialize and tune Gradient Boosting model (adopted as primary model)
param_grid_gb = {
    'n_estimators': [100, 200, 300],
    'learning_rate': [0.01, 0.05, 0.1],
    'max_depth': [3, 5, 7]
}
grid_search_gb = GridSearchCV(estimator=GradientBoostingRegressor(random_state=42),
                              param_grid=param_grid_gb,
                              cv=5,
                              scoring='neg_mean_squared_error',
                              n_jobs=-1)
grid_search_gb.fit(X_train, y_train)
best_gb_model = grid_search_gb.best_estimator_
print(f"Best Gradient Boosting hyperparameters: {grid_search_gb.best_params_}")


# Step 7: Train the best Gradient Boosting model on the full training set
best_gb_model.fit(X_train, y_train)


# Step 8: Make predictions on the test set
y_pred_gb = best_gb_model.predict(X_test)


# Step 9: Evaluate the tuned Gradient Boosting model on the test set
mse_gb = mean_squared_error(y_test, y_pred_gb)
r2_gb = r2_score(y_test, y_pred_gb)
print(f"Gradient Boosting Tuned Mean Squared Error (MSE): {mse_gb:.4f}")
print(f"Gradient Boosting Tuned R-squared: {r2_gb:.4f}")


# Step 10: Save the best Gradient Boosting model
joblib.dump(best_gb_model, 'best_gb_model.pkl')
print("Best Gradient Boosting model saved to 'best_gb_model.pkl'")


# Step 11: Feature Importance for Gradient Boosting
importances_gb = best_gb_model.feature_importances_
feature_names = X_train.columns
feature_importance_df_gb = pd.DataFrame({'Feature': feature_names, 'Importance': importances_gb})
feature_importance_df_gb = feature_importance_df_gb.sort_values(by='Importance', ascending=False)
print("\nTop 5 Most Important Features (Gradient Boosting):")
print(feature_importance_df_gb.head())


# Plot feature importances
plt.figure(figsize=(10, 6))
plt.barh(feature_importance_df_gb['Feature'], feature_importance_df_gb['Importance'], color='lightgreen')
plt.xlabel('Importance')
plt.ylabel('Feature')
plt.title('Feature Importances from Gradient Boosting')
plt.gca().invert_yaxis()
plt.savefig('feature_importances_gb.png')  # Save plot as PNG
# plt.show() removed to avoid warnings in non-interactive environment


# Step 12: Residual Analysis for Gradient Boosting
residuals_gb = y_test - y_pred_gb


# Plot predicted vs. actual values
plt.figure(figsize=(8, 6))
plt.scatter(y_test, y_pred_gb, alpha=0.5)
plt.plot([min(y_test), max(y_test)], [min(y_test), max(y_test)], 'r--')  # 45-degree line
plt.xlabel('Actual SFR')
plt.ylabel('Predicted SFR')
plt.title('Predicted vs. Actual Star Formation Rates (Gradient Boosting)')
plt.savefig('predicted_vs_actual_gb.png')  # Save plot as PNG


# Plot histogram of residuals
plt.figure(figsize=(8, 6))
plt.hist(residuals_gb, bins=30, edgecolor='black')
plt.xlabel('Residuals (Actual - Predicted)')
plt.ylabel('Frequency')
plt.title('Histogram of Residuals (Gradient Boosting)')
plt.savefig('residuals_histogram_gb.png')  # Save plot as PNG


# Plot residuals vs. predicted values
plt.figure(figsize=(8, 6))
plt.scatter(y_pred_gb, residuals_gb, alpha=0.5)
plt.axhline(y=0, color='red', linestyle='--')
plt.xlabel('Predicted Values')
plt.ylabel('Residuals (Actual - Predicted)')
plt.title('Residuals vs. Predicted Values (Gradient Boosting)')
plt.savefig('residuals_vs_predicted_gb.png')  # Save plot as PNG


# Step 13: Tune XGBoost for comparison
param_grid_xgb = {
    'n_estimators': [100, 200, 300],
    'learning_rate': [0.01, 0.05, 0.1],
    'max_depth': [3, 5, 7]
}
grid_search_xgb = GridSearchCV(estimator=xgb.XGBRegressor(random_state=42),
                               param_grid=param_grid_xgb,
                               cv=5,
                               scoring='neg_mean_squared_error',
                               n_jobs=-1)
grid_search_xgb.fit(X_train, y_train)
best_xgb_model = grid_search_xgb.best_estimator_
y_pred_xgb = best_xgb_model.predict(X_test)
mse_xgb = mean_squared_error(y_test, y_pred_xgb)
r2_xgb = r2_score(y_test, y_pred_xgb)
print(f"\nTuned XGBoost MSE: {mse_xgb:.4f}")
print(f"Tuned XGBoost R-squared: {r2_xgb:.4f}")


# Step 14: Summarize Model Performance
print("\nModel Performance Summary:")
print(f"Gradient Boosting - MSE: {mse_gb:.4f}, R-squared: {r2_gb:.4f}")
print(f"XGBoost - MSE: {mse_xgb:.4f}, R-squared: {r2_xgb:.4f}")
