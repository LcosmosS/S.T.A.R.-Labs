features = base_features + [
    "mass_metallicity", "dust_metallicity", "disp_mass_ratio", 
    "age_metallicity", "sqrt_Re_kpc", "log_mass", "BSD_likelihood", 
    "cosmo_rank", "L_cosmo_s0.5", "L_cosmo_s1.0", "L_cosmo_s1.5", 
    "L_cosmo_s2.0", "cosmo_rank_L"
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


# Symbolic Regression with PySR
symbolic_model = PySRRegressor(
    model_selection="best",
    niterations=40,
    binary_operators=["+", "-", "*", "/", "^2"],
    unary_operators=["exp", "log", "sqrt", "sin", "cos"],
    extra_sympy_mappings={"log": lambda x: np.log(np.abs(x) + 1e-5), "^2": lambda x: x**2},
    loss="loss(x, y) = (x - y)^2",
    maxsize=25,
    parsimony=0.0001,
    verbosity=1,
    random_state=42,
    procs=1
)
symbolic_model.fit(X_train_scaled, y_train)
y_pred_sym = symbolic_model.predict(X_test_scaled)
r2_sym = r2_score(y_test, y_pred_sym)
print(f"PySR R²: {r2_sym:.4f}")
print("Top PySR Equations:\n", symbolic_model.equations_.head())


# Save symbolic expression as polynomial fit plot
x = np.linspace(min(y_test), max(y_test), 500)
y_expr = symbolic_model.predict(scaler.transform(np.tile(X_test.mean().values, (500,1))))
p = Polynomial.fit(y_test, y_pred_sym, deg=3)
plt.plot(*p.linspace(), label="Polynomial Fit")
plt.scatter(y_test, y_pred_sym, s=10, alpha=0.5, label="Symbolic Predictions")
plt.xlabel("True log_SFR_Ha")
plt.ylabel("Predicted log_SFR_Ha")
plt.title("Symbolic Regression Fit")
plt.legend()
plt.tight_layout()
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
plt.clf()


# Residuals and Correlation Analysis
residuals = pd.DataFrame({
    "True": y_test,
    "RF": y_pred_rf - y_test,
    "GB": y_pred_gb - y_test,
    "Symbolic": y_pred_sym - y_test,
    "cosmo_rank": X_test["cosmo_rank"],
    "L_cosmo_s1": X_test["L_cosmo_s1.0"]
})
sns.scatterplot(data=residuals, x="True", y="Symbolic", hue="cosmo_rank", size="L_cosmo_s1", alpha=0.6)
plt.axhline(0, color="black", linestyle="--")
plt.title("Symbolic Residuals vs True log_SFR_Ha")
plt.savefig("residuals_sym.png")
plt.clf()


print("Correlation of BSD Features with Residuals:")
print(residuals[["RF", "GB", "Symbolic", "cosmo_rank", "L_cosmo_s1"]].corr()[["RF", "GB", "Symbolic"]])
