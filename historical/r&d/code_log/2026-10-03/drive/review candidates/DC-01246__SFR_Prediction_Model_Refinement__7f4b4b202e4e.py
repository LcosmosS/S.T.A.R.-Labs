print(f"R² Score: {r2}")


# Step 10: Use SHAP to explain the model's predictions
explainer = shap.TreeExplainer(model)
shap_values = explainer.shap_values(X_test_scaled)


# Visualize the SHAP summary plot
shap.summary_plot(shap_values, X_test)


# Optionally, you can visualize the impact of specific features
shap.dependence_plot('log_Mass', shap_values, X_test)


# Save the merged data if needed
df1.to_csv('merged_output.csv', index=False)


# Optional: Print the first few rows to verify the merged data
print(df1.head())
