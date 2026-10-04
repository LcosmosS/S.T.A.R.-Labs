import shap


explainer = shap.Explainer(gb, X_test)
shap_values = explainer(X_test, check_additivity=False)  # ← this solves the issue
