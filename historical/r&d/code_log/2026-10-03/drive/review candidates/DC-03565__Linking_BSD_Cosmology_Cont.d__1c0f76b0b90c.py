import pandas as pd


# Get feature importances
importances = rf_model.feature_importances_
feature_names = X_train.columns  # Replace with your feature names
feature_importance_df = pd.DataFrame({'Feature': feature_names, 'Importance': importances})
feature_importance_df = feature_importance_df.sort_values(by='Importance', ascending=False)
print(feature_importance_df)
