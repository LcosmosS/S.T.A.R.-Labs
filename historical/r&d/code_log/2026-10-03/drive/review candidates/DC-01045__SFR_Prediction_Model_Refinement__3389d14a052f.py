# SHAP interaction values (a bit more computationally expensive)
print("Calculating SHAP interaction values...")
interaction_values = shap.TreeExplainer(gb).shap_interaction_values(X_test)


# Visualize interaction between BSD_likelihood and another top feature
shap.dependence_plot("BSD_likelihood", shap_values.values, X_test, interaction_index='logmstar')
