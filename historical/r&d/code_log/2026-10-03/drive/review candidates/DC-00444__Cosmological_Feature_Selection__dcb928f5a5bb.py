# Derived & interaction features
df["color_ug"] = df["u"] - df["g"]
df["color_gr"] = df["g"] - df["r"]
df["color_ri"] = df["r"] - df["i"]
df["color_iz"] = df["i"] - df["z"]
df["mag_ratio"] = df["r"] / (df["i"] + 1e-5)
df["redshift_morph"] = df["redshift"] * df["t01_smooth_or_features_a01_smooth_fraction"]
df["cosmo_rank_mag"] = df["cosmo_rank"] * df["r"]


# Combine features
features = base_features + [
    "color_ug", "color_gr", "color_ri", "color_iz", "mag_ratio", 
    "redshift_morph", "cosmo_rank_mag", "cosmo_rank", 
    "L_cosmo_s0.5", "L_cosmo_s1.0", "L_cosmo_s1.5", "L_cosmo_s2.0"
]


X = df[features]
y = df[target]


# Step 6: Train/test split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)


# Step 7: Normalize features
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)


# Step 8: Random Forest
rf = RandomForestRegressor(n_estimators=200, max_depth=12, random_state=42)
rf.fit(X_train_scaled, y_train)
y_pred_rf = rf.predict(X_test_scaled)
r2_rf = r2_score(y_test, y_pred_rf)


# Step 9: Gradient Boosting
gb = GradientBoostingRegressor(n_estimators=300, learning_rate=0.05, max_depth=6, random_state=42)
gb.fit(X_train_scaled, y_train)
y_pred_gb = gb.predict(X_test_scaled)
r2_gb = r2_score(y_test, y_pred_gb)


print(f"R^2 Score (Random Forest): {r2_rf:.4f}")
print(f"R^2 Score (Gradient Boosting): {r2_gb:.4f}")


# Step 10: SHAP Analysis (optional, requires computational resources)
explainer_rf = shap.Explainer(rf, X_train_scaled)
shap_values_rf = explainer_rf(X_test_scaled)
shap.summary_plot(shap_values_rf, X_test_scaled, plot_type="bar", show=False)
plt.title("SHAP Summary - Random Forest")
plt.tight_layout()
plt.savefig("shap_rf_summary.png")
plt.clf()


# Step 11: Symbolic Regression (optional)
symbolic_model = SymbolicRegressor(
    population_size=1000, generations=20, stopping_criteria=0.01,
    p_crossover=0.7, p_subtree_mutation=0.1, p_hoist_mutation=0.05,
    p_point_mutation=0.1, max_samples=0.9, verbose=1, parsimony_coefficient=0.01,
    random_state=42
)
symbolic_model.fit(X_train_scaled, y_train)
y_pred_sym = symbolic_model.predict(X_test_scaled)
print("Symbolic Expression:")
print(symbolic_model._program)


# Plot predictions (optional)
plt.scatter(y_test, y_pred_rf, alpha=0.5, label="RF", marker="o")
plt.scatter(y_test, y_pred_gb, alpha=0.5, label="GB", marker="s")
plt.scatter(y_test, y_pred_sym, alpha=0.5, label="Symbolic", marker="^")
plt.plot([y.min(), y.max()], [y.min(), y.max()], "k--")
plt.xlabel("True t01_smooth_or_features_a01_smooth_fraction")
plt.ylabel("Predicted")
plt.legend()
plt.savefig("predictions.png")
plt.close()
