print(f"R² Score: {r2}")


# Step 10: Use SHAP to explain the model's predictions
# Create a SHAP explainer object
explainer = shap.TreeExplainer(model)


# Calculate SHAP values for the test set
shap_values = explainer.shap_values(X_test_scaled)


# Visualize the SHAP summary plot
shap.summary_plot(shap_values, X_test)


# Optionally, you can visualize the impact of specific features
# Example: SHAP dependence plot for 'log_Mass'
shap.dependence_plot('log_Mass', shap_values, X_test)


# Save the merged data if needed
merged_df.to_csv('merged_output.csv', index=False)


# Optional: Print the first few rows of the merged data to verify
print(merged_df.head())
