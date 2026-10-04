import shap


# Create a SHAP explainer object for the model
explainer = shap.TreeExplainer(model)


# Calculate SHAP values for the test set
shap_values = explainer.shap_values(X_test_scaled)


# Visualize the SHAP summary plot
shap.summary_plot(shap_values, X_test)
