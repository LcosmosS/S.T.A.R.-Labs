mse = mean_squared_error(y_test, y_pred) r2 = r2_score(y_test, y_pred)
print(f"Baseline Mean Squared Error (MSE): {mse:.4f}") print(f"Baseline R-squared: {r2:.4f}")
