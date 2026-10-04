# Initialize the model (example: Random Forest)
model = RandomForestRegressor(random_state=42)
# Perform cross-validation and calculate MSE for each fold
mse_scores = cross_val_score(model, X, y, cv=kf, scoring='neg_mean_squared_error') mse_scores = -mse_scores # Convert to positive MSE
# Print results
print(f"MSE for each fold: {mse_scores}") print(f"Average MSE: {np.mean(mse_scores):.4f}")
