cv_r2_gb = \ncross_val_score(gb, X, y, cv=5, scoring=\'r2\').mean() cv_mse_rf = -
cross_val_score(rf, X, y, \ncv=5, scoring=\'neg_mean_squared_error\').mean()
cv_r2_rf = cross_val_score(rf, X, y, cv=5, \nscoring=\'r2\').mean() print(f"CrossValidation MSE (Gradient Boosting): {cv_mse_gb:.4f}, R²: \n{cv_r2_gb:.4f}")
print(f"Cross-Validation MSE (Random Forest): {cv_mse_rf:.4f}, R²: \n{cv_r2_rf:.4f}")
# --- Visualize Results --- # Residual Plot for Random Forest plt.figure(figsize=(8,
\n\n6)) residuals_rf = y_test - y_pred_rf plt.scatter(y_pred_rf, residuals_rf, alpha=0.5)
plt.axhline(0, \ncolor=\'red\', linestyle=\'--\') plt.xlabel(\'Predicted SFR\')
plt.ylabel(\'Residuals\') plt.title(\'Residuals vs \nPredicted SFR (Random Forest)\')
plt.show() # Feature Importance for Random Forest \nplt.figure(figsize=(8, 6))
importances = rf.feature_importances_ feature_names = X.columns \nsorted_idx =
importances.argsort() plt.barh(feature_names[sorted_idx], importances[sorted_idx])
\nplt.xlabel(\'Importance\') plt.title(\'Feature Importances (Random Forest)\')
plt.show() \nChatGPT said: \nThanks for sharing your code and the new file (model
