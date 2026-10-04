# For Random Forest
explainer_rf = shap.TreeExplainer(best_rf_model)
shap_values_rf = explainer_rf.shap_values(X_test_scaled)


# For Gradient Boosting
explainer_gb = shap.TreeExplainer(best_gb_model)
shap_values_gb = explainer_gb.shap_values(X_test_scaled)


# Plot SHAP summary for Random Forest
shap.summary_plot(shap_values_rf, X_test)


# Plot SHAP summary for Gradient Boosting
shap.summary_plot(shap_values_gb, X_test)


# Optional: Save the merged data with SFR if needed
df1.to_csv('merged_output_with_SFR.csv', index=False)


# Print the first few rows to verify the merged data
print(df1.head())
