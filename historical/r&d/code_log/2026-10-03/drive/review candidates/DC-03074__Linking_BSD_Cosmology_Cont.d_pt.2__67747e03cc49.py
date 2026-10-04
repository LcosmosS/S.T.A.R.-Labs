import pandas as pd import matplotlib.pyplot as plt
# Assuming 'best_model' is your trained Random Forest model # and 'X_train' is the training feature set # Get feature importances
importances = best_model.feature_importances_ feature_names = X_train.columns # Replace with your feature names
# Create a DataFrame for easier visualization
feature_importance_df = pd.DataFrame({'Feature': feature_names, 'Importance': importances}) feature_importance_df = feature_importance_df.sort_values(by='Importance', ascending=False)
# Print the top 5 most important features
print("Top 5 Most Important Features:") print(feature_importance_df.head())
# Optional: Plot the feature importances
plt.figure(figsize=(10, 6)) plt.barh(feature_importance_df['Feature'], feature_importance_df['Importance'], color='skyblue') plt.xlabel('Importance') plt.ylabel('Feature') plt.title('Feature Importances from Random Forest') plt.gca().invert_yaxis() # Highest importance at the top plt.savefig('feature_importances.png') plt.show()
