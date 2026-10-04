import pandas as pd import matplotlib.pyplot as plt
# Assume 'best_model' is your trained Random Forest model # and 'X_train' is your training data with 15 predictors
importances = best_model.feature_importances_ feature_names = X_train.columns # Your 15 predictor names
# Create a DataFrame for sorting and visualization
feature_importance_df = pd.DataFrame({ 'Feature': feature_names, 'Importance': importances }) feature_importance_df = feature_importance_df.sort_values(by='Importance', ascending=False)
# Display the top 5 most important features
print("Top 5 Most Important Features:") print(feature_importance_df.head())
# Plot feature importances
plt.figure(figsize=(10, 6)) plt.barh(feature_importance_df['Feature'], feature_importance_df['Importance'], color='skyblue') plt.xlabel('Importance') plt.ylabel('Feature') plt.title('Feature Importances from Random Forest') plt.gca().invert_yaxis() # Put the most important feature at the top plt.savefig('feature_importances.png') # Save the plot plt.show()
