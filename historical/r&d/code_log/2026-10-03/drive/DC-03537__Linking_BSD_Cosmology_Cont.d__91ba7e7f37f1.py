from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, r2_score


# Initialize the Random Forest Regressor
rf_model = RandomForestRegressor(random_state=42)


# Train the model (assuming X_train and y_train are your features and target)
rf_model.fit(X_train, y_train)


# Make predictions on the testing set
y_pred = rf_model.predict(X_test)


# Evaluate performance
mse = mean_squared_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)
print(f"Mean Squared Error (MSE): {mse:.4f}")
print(f"R-squared: {r2:.4f}")
* Why: This baseline helps you establish a starting point. For example, if you previously had an MSE of 0.4266, you can compare it to this result to see if the cleaned dataset improves performance.
