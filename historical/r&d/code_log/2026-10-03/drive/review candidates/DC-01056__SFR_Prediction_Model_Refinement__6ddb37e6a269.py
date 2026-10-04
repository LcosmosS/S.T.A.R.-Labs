import shap
import joblib
import pandas as pd


# Load trained Gradient Boosting model
gb = joblib.load("model/gradient_boosting_model.pkl")


# Load your test data
X_test = pd.read_csv("data/X_test.csv")  # adjust this path to where your test data is


# Initialize the explainer
explainer = shap.Explainer(gb, X_test)


# Get SHAP values
shap_values = explainer(X_test, check_additivity=False)


# Summary plot
shap.summary_plot(shap_values, X_test, plot_type="bar")
