importances = rf_model.feature_importances_
feature_names = X_train.columns
feature_importance_df = pd.DataFrame({'Feature': feature_names, 'Importance': importances})
feature_importance_df = feature_importance_df.sort_values(by='Importance', ascending=False)
print(feature_importance_df)
* Why it matters: Identifying the most important features allows you to focus on refining or adding similar data points, potentially improving the model’s accuracy.
