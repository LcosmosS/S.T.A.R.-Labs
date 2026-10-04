import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.model_selection import GridSearchCV, train_test_split
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.metrics import mean_squared_error, r2_score
import joblib
import xgboost as xgb


# Step 1: Load the dataset
df = pd.read_csv('filtered_Pipe3D.csv')  # Replace with your dataset file path
print(f"Dataset loaded with {len(df)} rows and {len(df.columns)} columns.")


# Step 2: Define features (X) and target (y)
X = df.drop(columns=['log_SFR_Ha'])  # Replace 'log_SFR_Ha' with your target column
y = df['log_SFR_Ha']


# Step 3: Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
print(f"Training set: {X_train.shape[0]} rows, Testing set: {X_test.shape[0]} rows")


# Step 4: Adopt Gradient Boosting as the Primary Model
# Train the initial Gradient Boosting model
gb_model = GradientBoostingRegressor(random_state=42)
gb_model.fit(X_train, y_train)


# Make predictions
y_pred_gb = gb_model.predict(X_test)


# Evaluate the model
mse_gb = mean_squared_error(y_test, y_pred_gb)
r2_gb = r2_score(y_test, y_pred_gb)
print(f"Gradient Boosting (Untuned) MSE: {mse_gb:.4f}")
print(f"Gradient Boosting (Untuned) R-squared: {r2_gb:.4f}")


# Save the untuned model
joblib.dump(gb_model, 'best_gb_model.pkl')
print("Untuned Gradient Boosting model saved to 'best_gb_model.pkl'")


# Step 5: Tune Gradient Boosting Hyperparameters
param_grid_gb = {
    'n_estimators': [100, 200, 300],
    'learning_rate': [0.01, 0.05, 0.1],
    'max_depth': [3, 5, 7]
}
grid_search_gb = GridSearchCV(estimator=GradientBoostingRegressor(random_state=42),
                              param_grid=param_grid_gb, cv=5, scoring='neg_mean_squared_error', n_jobs=-1)
grid_search_gb.fit(X_train, y_train)
print(f"Best Gradient Boosting hyperparameters: {grid_search_gb.best_params_}")


# Train and evaluate the tuned Gradient Boosting model
best_gb_model = grid_search_gb.best_estimator_
best_gb_model.fit(X_train, y_train)
y_pred_gb_tuned = best_gb_model.predict(X_test)
mse_gb_tuned = mean_squared_error(y_test, y_pred_gb_tuned)
r2_gb_tuned = r2_score(y_test, y_pred_gb_tuned)
print(f"Tuned Gradient Boosting MSE: {mse_gb_tuned:.4f}")
print(f"Tuned Gradient Boosting R-squared: {r2_gb_tuned:.4f}")


# Save the tuned model
joblib.dump(best_gb_model, 'best_tuned_gb_model.pkl')
print("Tuned Gradient Boosting model saved to 'best_tuned_gb_model.pkl'")


# Step 6: Leverage Feature Importances
# Check for log_Mass and create an interaction term with log_Mass_gas
if 'log_Mass' in X.columns and 'log_Mass_gas' in X.columns:
    X['interaction_log_Mass_gas_log_Mass'] = X['log_Mass_gas'] * X['log_Mass']
    print("Added interaction term: log_Mass_gas * log_Mass")
else:
    print("One or both of 'log_Mass' and 'log_Mass_gas' not found. Consider adding gas-related features.")


# Step 7: Residual Analysis (Saved Plots)
# Calculate residuals from the tuned Gradient Boosting model
residuals_gb = y_test - y_pred_gb_tuned


# Plot 1: Predicted vs. Actual Values
plt.figure(figsize=(8, 6))
plt.scatter(y_test, y_pred_gb_tuned, alpha=0.5)
plt.plot([min(y_test), max(y_test)], [min(y_test), max(y_test)], 'r--')  # 45-degree line
plt.xlabel('Actual SFR')
plt.ylabel('Predicted SFR')
plt.title('Predicted vs. Actual SFR (Tuned Gradient Boosting)')
plt.savefig('predicted_vs_actual_gb.png')
plt.close()  # Close the figure to free memory


# Plot 2: Histogram of Residuals
plt.figure(figsize=(8, 6))
plt.hist(residuals_gb, bins=30, edgecolor='black')
plt.xlabel('Residuals (Actual - Predicted)')
plt.ylabel('Frequency')
plt.title('Histogram of Residuals (Tuned Gradient Boosting)')
plt.savefig('residuals_histogram_gb.png')
plt.close()


# Plot 3: Residuals vs. Predicted Values
plt.figure(figsize=(8, 6))
plt.scatter(y_pred_gb_tuned, residuals_gb, alpha=0.5)
plt.axhline(y=0, color='red', linestyle='--')
plt.xlabel('Predicted Values')
plt.ylabel('Residuals (Actual - Predicted)')
plt.title('Residuals vs. Predicted Values (Tuned Gradient Boosting)')
plt.savefig('residuals_vs_predicted_gb.png')
plt.close()


print("Residual plots saved as 'predicted_vs_actual_gb.png', 'residuals_histogram_gb.png', and 'residuals_vs_predicted_gb.png'")


# Step 8: Improve XGBoost Performance
param_grid_xgb = {
    'n_estimators': [100, 200, 300],
    'learning_rate': [0.01, 0.05, 0.1],
    'max_depth': [3, 5, 7]
}
grid_search_xgb = GridSearchCV(estimator=xgb.XGBRegressor(random_state=42),
                               param_grid=param_grid_xgb, cv=5, scoring='neg_mean_squared_error', n_jobs=-1)
grid_search_xgb.fit(X_train, y_train)
best_xgb_model = grid_search_xgb.best_estimator_
y_pred_xgb_tuned = best_xgb_model.predict(X_test)
mse_xgb_tuned = mean_squared_error(y_test, y_pred_xgb_tuned)
r2_xgb_tuned = r2_score(y_test, y_pred_xgb_tuned)
print(f"Tuned XGBoost MSE: {mse_xgb_tuned:.4f}")
print(f"Tuned XGBoost R-squared: {r2_xgb_tuned:.4f}")


# Save the tuned XGBoost model
joblib.dump(best_xgb_model, 'best_tuned_xgb_model.pkl')
print("Tuned XGBoost model saved to 'best_tuned_xgb_model.pkl'")


# Step 9: Summary of Model Performance
print("\nModel Performance Summary:")
print(f"Gradient Boosting (Untuned) - MSE: {mse_gb:.4f}, R-squared: {r2_gb:.4f}")
print(f"Gradient Boosting (Tuned) - MSE: {mse_gb_tuned:.4f}, R-squared: {r2_gb_tuned:.4f}")
print(f"XGBoost (Tuned) - MSE: {mse_xgb_tuned:.4f}, R-squared: {r2_xgb_tuned:.4f}")
