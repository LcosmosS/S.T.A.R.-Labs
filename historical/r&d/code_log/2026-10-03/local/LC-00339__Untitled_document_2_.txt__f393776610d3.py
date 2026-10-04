mse_refined = mean_squared_error(y_test, y_pred_refined) r2_refined = r2_score(y_test, y_pred_refined)
print(f"Refined MSE: {mse_refined:.4f}") print(f"Refined R-squared: {r2_refined:.4f}")
importances = refined_rf_model.feature_importances_ feature_names = X.columns feature_importance_df = pd.DataFrame({'Feature': feature_names, 'Importance': importances}) feature_importance_df = feature_importance_df.sort_values(by='Importance', ascending=False)
print("Feature Importances:") print(feature_importance_df)
import joblib
