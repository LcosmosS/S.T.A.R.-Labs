import shap
import matplotlib.pyplot as plt
import joblib


# Load model and data
print("Loading model and data...")
gb = joblib.load("gb_model.pkl")
X_test = joblib.load("X_test.pkl")


# Initialize SHAP explainer
print("Initializing SHAP explainer...")
explainer = shap.Explainer(gb, X_test)
shap_values = explainer(X_test)


# Generate summary plot
print("Generating SHAP summary plot...")
shap.summary_plot(shap_values, X_test, plot_type="dot", show=False)


# Show or save plot
plt.show()
# plt.savefig("shap_summary_plot.png")
