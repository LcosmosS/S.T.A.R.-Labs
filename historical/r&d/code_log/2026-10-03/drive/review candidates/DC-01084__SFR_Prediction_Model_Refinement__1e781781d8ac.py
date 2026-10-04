import shap


# Create SHAP explainer
explainer = shap.Explainer(gb, X_train)


# Compute SHAP values for the test set
shap_values = explainer(X_test)


# Plot the summary
shap.summary_plot(shap_values, X_test)
