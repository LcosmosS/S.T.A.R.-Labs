# BSD-inspired symbolic functions (cosmological analogues to L-functions or rank equations)
df["L_cosmo"] = df["log_Mass_gas"] * df["cosmo_rank"] / (df["Age_LW_Re_fit"] + 1e-5)
df["BSD_signature"] = (df["OH_T04_cen"]**2 + df["Lambda_Re"]) / (df["Re_kpc"] + 1e-5)
df["R_gal"] = (df["log_Mass_gas"] * df["OH_O3N2_cen"] * df["Lambda_Re"]) / (
    df["Av_gas_Re"] * df["ZH_LW_Re_fit"] + 1e-5)


features = base_features + [
    "mass_metallicity", "dust_metallicity", "disp_mass_ratio", 
    "age_metallicity", "sqrt_Re_kpc", "log_mass", 
    "BSD_likelihood", "cosmo_rank",
    "L_cosmo", "BSD_signature", "R_gal"
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


# PySR Symbolic Regression
X_pysr = X_train.copy()
X_pysr["target"] = y_train


model = PySRRegressor(
    model_selection="best",
    niterations=100,
    binary_operators=["+", "-", "*", "/"],
    unary_operators=["exp", "log", "sqrt"],
    extra_sympy_mappings={"log": lambda x: np.log(np.abs(x) + 1e-5)},
    loss="loss(x, y) = (x - y)^2",
    maxsize=20,
    verbosity=1,
    random_state=42,
)


model.fit(X_train, y_train)
print(model)


# Plot predictions vs true
y_pred_sym = model.predict(X_test)
plt.scatter(y_test, y_pred_rf, alpha=0.5, label="RF", marker="o")
plt.scatter(y_test, y_pred_gb, alpha=0.5, label="GB", marker="s")
plt.scatter(y_test, y_pred_sym, alpha=0.5, label="PySR", marker="^")
plt.plot([y.min(), y.max()], [y.min(), y.max()], "k--")
plt.xlabel("True log_SFR_Ha")
plt.ylabel("Predicted")
plt.title("Model Predictions vs True Values")
plt.legend()
plt.tight_layout()
plt.savefig("model_comparison.png")
