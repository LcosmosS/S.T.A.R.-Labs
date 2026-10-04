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
