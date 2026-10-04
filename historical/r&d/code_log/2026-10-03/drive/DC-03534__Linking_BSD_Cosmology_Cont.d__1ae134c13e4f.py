from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, r2_score


# Initialize the Random Forest Regressor with default hyperparameters
rf_model = RandomForestRegressor(random_state=42)


# Train the model on the training set
rf_model.fit(X_train, y_train)


# Make predictions on the testing set
y_pred = rf_model.predict(X_test)


# Evaluate the model's performance
mse = mean_squared_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)


print(f"Baseline Mean Squared Error (MSE): {mse:.4f}")
print(f"Baseline R-squared: {r2:.4f}")
* Why it matters: This gives you a starting point (baseline) for model performance. Your previous MSE was 0.4266; compare this baseline to see if the cleaned dataset improves results.
