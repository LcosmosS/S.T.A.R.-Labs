# Initialize the Random Forest model
rf_model = RandomForestRegressor(random_state=42)


# Perform cross-validation and calculate MSE for each fold
mse_scores = cross_val_score(rf_model, X, y, cv=kf, scoring='neg_mean_squared_error')
mse_scores = -mse_scores  # Convert to positive MSE


# Print the MSE for each fold and the average MSE
print(f"MSE for each fold: {mse_scores}")
print(f"Average MSE: {np.mean(mse_scores):.4f}")
