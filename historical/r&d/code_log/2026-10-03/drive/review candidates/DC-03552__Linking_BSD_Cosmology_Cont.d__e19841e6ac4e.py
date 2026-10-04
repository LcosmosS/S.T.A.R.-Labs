import seaborn as sns


plt.figure(figsize=(10, 6))
sns.barplot(x='Importance', y='Feature', data=feature_importance_df)
plt.title('Feature Importances')
plt.savefig('feature_importance.png')
* plt.show()
