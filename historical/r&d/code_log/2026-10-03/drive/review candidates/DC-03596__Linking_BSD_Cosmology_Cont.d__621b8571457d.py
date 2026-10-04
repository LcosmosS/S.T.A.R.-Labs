from sklearn.ensemble import GradientBoostingRegressor
from sklearn.metrics import mean_squared_error, r2_score


# Train Gradient Boosting model
gb_model = GradientBoostingRegressor(random_state=42)
gb_model.fit(X_train, y_train)


# Predict on test set
y_pred_gb = gb_model.predict(X_test)


# Evaluate performance
mse_gb = mean_squared_error(y_test, y_pred_gb)
r2_gb = r2_score(y_test, y_pred_gb)
print(f"Gradient Boosting MSE: {mse_gb:.4f}")
print(f"Gradient Boosting R-squared: {r2_gb:.4f}")


# Compare to Random Forest (replace with your RF metrics)
print("Random Forest MSE: 0.2743")  # Example value
print("Random Forest R-squared: 0.8217")  # Example value
