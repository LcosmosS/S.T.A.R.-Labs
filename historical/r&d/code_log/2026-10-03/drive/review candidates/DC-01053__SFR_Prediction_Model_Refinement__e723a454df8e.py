import shap


# Initialize TreeExplainer
explainer = shap.Explainer(gb, X_test)


# Get SHAP values (disable strict check)
shap_values = explainer(X_test, check_additivity=False)


# Plot summary (bar chart)
shap.summary_plot(shap_values, X_test, plot_type="bar")
