import shap
explainer = shap.Explainer(gb_model)
shap_values = explainer(X_test)
shap.plots.beeswarm(shap_values)
