import shap


# Create SHAP explainer for your Gradient Boosting model
explainer = shap.Explainer(gb, X_test)


# Compute SHAP values without triggering additivity error
shap_values = explainer(X_test, check_additivity=False)


# Plot feature importance (bar chart)
shap.summary_plot(shap_values, X_test, plot_type="bar")
