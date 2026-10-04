print(f"R² Score: {r2}")


# --- SHAP Analysis ---
# Ensure that SHAP uses the same data shape as the model training
explainer = shap.TreeExplainer(model)


# Calculate SHAP values for the test set
shap_values = explainer.shap_values(X_test_scaled)


# Visualize the SHAP summary plot
shap.summary_plot(shap_values, X_test)


# Optionally, you can visualize the impact of specific features
shap.dependence_plot('ra', shap_values, X_test)


# Save the merged data with SFR if needed
df1.to_csv('merged_output_with_SFR.csv', index=False)


# Optional: Print the first few rows to verify the merged data
print(df1.head())
