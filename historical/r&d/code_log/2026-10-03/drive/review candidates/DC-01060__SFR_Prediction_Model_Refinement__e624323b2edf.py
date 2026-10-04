import matplotlib.pyplot as plt


shap.summary_plot(shap_values, X_test, plot_type="bar", show=False)
plt.savefig("shap_summary_plot.png", bbox_inches="tight")
