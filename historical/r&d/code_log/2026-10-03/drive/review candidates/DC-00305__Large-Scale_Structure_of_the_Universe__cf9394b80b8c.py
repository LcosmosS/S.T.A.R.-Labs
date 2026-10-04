# Feature importance for Random Forest
importances_rf = rf_model.feature_importances_
for feature, importance in zip(X.columns, importances_rf):
    print(f"Feature: {feature}, Importance: {importance}")


# Feature importance for Gradient Boosting
importances_gb = gb_model.feature_importances_
for feature, importance in zip(X.columns, importances_gb):
    print(f"Feature: {feature}, Importance: {importance}")
