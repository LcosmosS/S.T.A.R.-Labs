# Make predictions on the testing set
y_pred = best_rf_model.predict(X_test)


# Calculate MSE and R-squared
mse = mean_squared_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)
print(f"Tuned Mean Squared Error (MSE): {mse:.4f}")
print(f"Tuned R-squared: {r2:.4f}")
