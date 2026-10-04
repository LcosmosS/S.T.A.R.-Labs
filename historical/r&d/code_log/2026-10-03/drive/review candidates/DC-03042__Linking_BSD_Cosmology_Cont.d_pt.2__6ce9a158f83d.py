from sklearn.metrics import mean_squared_error, r2_score
# Make predictions on the test set
y_pred = rf_model.predict(X_test)
# Calculate MSE and R-squared
mse = mean_squared_error(y_test, y_pred) r2 = r2_score(y_test, y_pred)
print(f"Initial MSE: {mse:.4f}") print(f"Initial R-squared: {r2:.4f}")
