# Compute residuals
residuals_rf = y_test - y_pred_rf


# Identify outliers with residuals > 2 or < -2
outlier_mask = (residuals_rf > 2) | (residuals_rf < -2)
outliers = X_test[outlier_mask].copy()
outliers['residual'] = residuals_rf[outlier_mask]
outliers['true_SFR'] = y_test[outlier_mask]
outliers['predicted_SFR'] = y_pred_rf[outlier_mask]


print("Number of residual outliers:", outliers.shape[0])
print(outliers.head())
