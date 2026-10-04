features = base_features + [
    "mass_metallicity", "dust_metallicity", "disp_mass_ratio", 
    "age_metallicity", "sqrt_Re_kpc", "log_mass", "BSD_likelihood", "cosmo_rank"
]


X = df[features]
y = df[target]


# Train/test split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)


# Normalize features
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)


# Random Forest
rf = RandomForestRegressor(n_estimators=200, max_depth=12, random_state=42)
rf.fit(X_train_scaled, y_train)
y_pred_rf = rf.predict(X_test_scaled)
r2_rf = r2_score(y_test, y_pred_rf)


# Gradient Boosting
gb = GradientBoostingRegressor(n_estimators=300, learning_rate=0.05, max_depth=6, random_state=42)
gb.fit(X_train_scaled, y_train)
y_pred_gb = gb.predict(X_test_scaled)
r2_gb = r2_score(y_test, y_pred_gb)


print(f"R^2 Score (Random Forest): {r2_rf:.4f}")
print(f"R^2 Score (Gradient Boosting): {r2_gb:.4f}")


# SHAP
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


# Symbolic Regression with gplearn
symbolic_model = SymbolicRegressor(
    population_size=1000,
    generations=20,
    stopping_criteria=0.01,
    p_crossover=0.7,
    p_subtree_mutation=0.1,
    p_hoist_mutation=0.05,
    p_point_mutation=0.1,
    max_samples=0.9,
    verbose=1,
    parsimony_coefficient=0.01,
    random_state=42,
    n_jobs=-1
)
symbolic_model.fit(X_train_scaled, y_train)
y_pred_sym = symbolic_model.predict(X_test_scaled)


# Print the symbolic expression
print("Symbolic Expression:")
print(symbolic_model._program)


# Save symbolic expression plot
from sklearn.tree import plot_tree
fig = plt.figure()
plt.text(0.01, 0.5, str(symbolic_model._program), fontsize=10, wrap=True)
plt.axis('off')
plt.savefig("pysr_expression_plot.png")
plt.clf()


# Plot predictions vs true
plt.scatter(y_test, y_pred_rf, alpha=0.5, label="RF", marker="o")
plt.scatter(y_test, y_pred_gb, alpha=0.5, label="GB", marker="s")
plt.scatter(y_test, y_pred_sym, alpha=0.5, label="Symbolic", marker="^")
plt.plot([y.min(), y.max()], [y.min(), y.max()], "k--")
plt.xlabel("True log_SFR_Ha")
plt.ylabel("Predicted")
plt.title("Model Predictions vs True Values")
plt.legend()
plt.tight_layout()
plt.savefig("model_comparison.png")
