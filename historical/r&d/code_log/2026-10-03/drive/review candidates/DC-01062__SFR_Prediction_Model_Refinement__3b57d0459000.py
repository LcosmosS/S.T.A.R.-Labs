import shap
import matplotlib.pyplot as plt  # Required for showing or saving plots


# Explain the model's predictions using SHAP
print("Initializing SHAP explainer...")
explainer = shap.Explainer(gb, X_test)  # Ensure gb and X_test are defined before running this
shap_values = explainer(X_test)


# --- Summary Plot ---
print("Generating SHAP summary plot...")
shap.summary_plot(shap_values, X_test, plot_type="dot", show=False)


# Display plot in a standalone Python script
plt.show()


# Optional: Save plot
# plt.savefig("shap_summary_dot.png", bbox_inches="tight")
