print(f"R^2 Score (Random Forest, Test Set): {r2_rf:.4f}")
print(f"R^2 Score (Gradient Boosting, Test Set): {r2_gb:.4f}")

# SHAP for feature selection
explainer_rf = shap.Explainer(rf, X_train_scaled)
shap_values_rf = explainer_rf(X_test_scaled)
explainer_gb = shap.Explainer(gb, X_train_scaled)
shap_values_gb = explainer_gb(X_test_scaled)
shap.summary_plot(shap_values_rf, X_test_scaled, plot_type="bar", show=False)
plt.title("SHAP Summary - Random Forest")
plt.tight_layout()
plt.savefig("shap_rf_summary.png")
plt.clf()
shap.summary_plot(shap_values_gb, X_test_scaled, plot_type="bar", show=False)
plt.title("SHAP Summary - Gradient Boosting")
plt.tight_layout()
plt.savefig("shap_gb_summary.png")
plt.clf()

# Feature selection based on SHAP
shap_values_rf_mean = np.abs(shap_values_rf.values).mean(axis=0)
feature_importance = pd.DataFrame({"feature": features, "importance": shap_values_rf_mean})
feature_importance = feature_importance.sort_values("importance", ascending=False)
top_features = feature_importance["feature"].head(10).tolist()
bsd_features = ["cosmo_rank", "L_cosmo_s_1.0", "cosmo_rank_L", "cosmo_rank_scaled",
"L_cosmo_s1_scaled", "cosmo_rank_L_mass", "L_cosmo_s1_metallicity"]
for bsd_feature in bsd_features:
    if bsd_feature not in top_features:
        top_features.append(bsd_feature)
X_selected = df[top_features]
X_train_selected, X_test_selected, _, _ = train_test_split(X_selected, y, test_size=0.2,
random_state=42)
X_train_selected_scaled = scaler.fit_transform(X_train_selected)
X_test_selected_scaled = scaler.transform(X_test_selected)

# Symbolic Regression with gplearn
symbolic_model = SymbolicRegressor(
    population_size=3000,
    generations=150,
    stopping_criteria=0.01,
    p_crossover=0.7,
