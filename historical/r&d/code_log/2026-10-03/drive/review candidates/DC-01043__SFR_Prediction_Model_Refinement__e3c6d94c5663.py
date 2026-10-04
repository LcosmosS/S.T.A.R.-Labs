import shap


# Explain the model's predictions using SHAP
print("Initializing SHAP explainer...")
explainer = shap.Explainer(gb, X_test)  # For Gradient Boosting
shap_values = explainer(X_test)


# --- Summary Plot ---
print("Generating SHAP summary plot...")
shap.summary_plot(shap_values, X_test, plot_type="dot")
