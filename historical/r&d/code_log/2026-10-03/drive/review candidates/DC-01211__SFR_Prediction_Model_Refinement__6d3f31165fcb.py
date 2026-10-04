from sklearn.model_selection import cross_val_score


# Perform cross-validation for Gradient Boosting model
print("Cross-validation for Gradient Boosting model...")
cv_gb_r2 = cross_val_score(gb, X, y, cv=5, scoring='r2')
cv_gb_mse = cross_val_score(gb, X, y, cv=5, scoring='neg_mean_squared_error')


# Perform cross-validation for Random Forest model
print("Cross-validation for Random Forest model...")
cv_rf_r2 = cross_val_score(rf, X, y, cv=5, scoring='r2')
cv_rf_mse = cross_val_score(rf, X, y, cv=5, scoring='neg_mean_squared_error')


# Print cross-validation results
print("\nCross-Validation Results:")
print(f"Gradient Boosting - Average R²: {cv_gb_r2.mean():.4f}, Average MSE: {-cv_gb_mse.mean():.4f}")
print(f"Random Forest - Average R²: {cv_rf_r2.mean():.4f}, Average MSE: {-cv_rf_mse.mean():.4f}")
