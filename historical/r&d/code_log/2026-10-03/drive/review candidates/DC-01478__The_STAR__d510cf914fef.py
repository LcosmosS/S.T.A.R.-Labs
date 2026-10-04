if missing_features:
    print(f"Warning: The following features are missing from the dataset: {missing_features}")
else:
    print("All features present in the dataset.")


# Correlation heatmap of numeric features ================================================================================================================================================
plt.figure(figsize=(12, 10))
sns.heatmap(X.corr(), annot=False, cmap='coolwarm', vmin=-1, vmax=1)
plt.title("Correlation Heatmap of Features")
plt.savefig("feature_correlation_heatmap.png")
plt.close()


# Filter to numeric columns only =========================================================================================================================================================
