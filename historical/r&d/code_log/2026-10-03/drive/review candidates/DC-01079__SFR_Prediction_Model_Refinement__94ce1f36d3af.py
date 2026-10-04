import shap


# Explain the model's predictions using SHAP
explainer = shap.Explainer(gb, X_train)
shap_values = explainer(X_test)


# Summary plot
shap.summary_plot(shap_values, X_test)
