import shap


explainer = shap.Explainer(model, X_train)
shap_values = explainer(X_test)


shap.summary_plot(shap_values, X_test, show=False)
plt.savefig("shap_summary_testset.png", bbox_inches="tight")
