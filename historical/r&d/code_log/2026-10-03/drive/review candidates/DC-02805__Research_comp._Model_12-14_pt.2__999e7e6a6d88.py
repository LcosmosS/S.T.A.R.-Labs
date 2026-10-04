import shap
import matplotlib.pyplot as plt


# For Random Forest
explainer_rf = shap.TreeExplainer(best_rf)
shap_values_rf = explainer_rf.shap_values(X_test_scaled)
shap.summary_plot(shap_values_rf, X_test, feature_names=X.columns, show=False)
plt.savefig('shap_summary_rf.png')  # Save the plot as a PNG file
plt.close()  # Close the plot to free up memory


# For Gradient Boosting
explainer_gb = shap.TreeExplainer(best_gb)
shap_values_gb = explainer_gb.shap_values(X_test_scaled)
shap.summary_plot(shap_values_gb, X_test, feature_names=X.columns, show=False)
plt.savefig('shap_summary_gb.png')  # Save the plot as a PNG file
plt.close()  # Close the plot to free up memory
