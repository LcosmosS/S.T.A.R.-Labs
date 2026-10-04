# Make predictions with the refined model
y_pred_refined = refined_rf_model.predict(X_test)


# Calculate MSE and R-squared for the refined model
mse_refined = mean_squared_error(y_test, y_pred_refined)
r2_refined = r2_score(y_test, y_pred_refined)


print(f"Refined MSE: {mse_refined:.4f}")
print(f"Refined R-squared: {r2_refined:.4f}")
