import shap


# Initialize the explainer (works for tree-based models like Gradient Boosting)
explainer = shap.Explainer(gb, X_test)


# Get SHAP values
shap_values = explainer(X_test)


# Summary plot (bar chart of global feature importance)
shap.summary_plot(shap_values, X_test, plot_type="bar")
