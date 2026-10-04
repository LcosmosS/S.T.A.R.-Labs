from sklearn.metrics import mean_squared_error, r2_score


# Make predictions on the test set
y_pred = rf_model.predict(X_test)


# Calculate MSE and R-squared
mse = mean_squared_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)


print(f"Initial Mean Squared Error (MSE): {mse:.4f}")
print(f"Initial R-squared: {r2:.4f}")
* MSE: Measures the average squared difference between predicted and actual values (lower is better).
* R-squared: Indicates how well the model explains the variability of the target (closer to 1 is better).
