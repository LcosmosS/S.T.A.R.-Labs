from sklearn.ensemble import GradientBoostingRegressor


# Initialize and train the Gradient Boosting model
gb_model = GradientBoostingRegressor(random_state=42)
gb_model.fit(X_train, y_train)


# Make predictions on the test set
y_pred_gb = gb_model.predict(X_test)


# Evaluate performance
mse_gb = mean_squared_error(y_test, y_pred_gb)
r2_gb = r2_score(y_test, y_pred_gb)
print(f"Gradient Boosting MSE: {mse_gb:.4f}")
print(f"Gradient Boosting R-squared: {r2_gb:.4f}")
      * What to Do:
      * Compare the MSE and R-squared of the Gradient Boosting model to those of the Random Forest (e.g., MSE=0.2743, R²=0.8217).
      * If the alternative model performs better, consider tuning its hyperparameters or using it instead.
      * You can also try XGBoost, LightGBM, or other models similarly.
