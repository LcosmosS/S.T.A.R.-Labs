import shap


def run_shap(gb, X_test):
    explainer = shap.Explainer(gb, X_test)
    shap_values = explainer(X_test, check_additivity=False)
    shap.summary_plot(shap_values, X_test, plot_type="bar")
