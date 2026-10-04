plt.plot(np.linspace(0.5, 2, 50), L_vals)
plt.xlabel("s")
plt.ylabel("L_cosmo(s)")
plt.title("L_cosmo(s) Behavior")
plt.savefig("L_cosmo_curve.png")
plt.show()
plt.close()


# Step 4: Feature Engineering
target = "log_SFR_Ha"
base_features = [
    "log_Mass_gas", "log_Mass", "Av_gas_Re", "Av_ssp_Re", 
    "OH_O3N2_cen", "OH_T04_cen", "OH_dop_cen", "Age_LW_Re_fit", 
    "ZH_LW_Re_fit", "Re_kpc", "vel_disp_Ha_cen", "Lambda_Re", 
    "Sigma_Mass_Re", "EW_Ha_cen", "Ha_Hb_cen"
]


df["mass_metallicity"] = df["log_Mass"] * df["OH_O3N2_cen"]
df["dust_metallicity"] = df["Av_gas_Re"] * df["OH_T04_cen"]
df["disp_mass_ratio"] = df["vel_disp_Ha_cen"] / (df["Sigma_Mass_Re"] + 1e-5)
df["age_metallicity"] = df["Age_LW_Re_fit"] * df["ZH_LW_Re_fit"]
df["sqrt_Re_kpc"] = np.sqrt(df["Re_kpc"] + 1e-5)
df["BSD_likelihood"] = df["log_Mass_gas"] * df["OH_O3N2_cen"] / (df["Av_gas_Re"] + 1e-5 + df["Age_LW_Re_fit"])
df["cosmo_rank_L"] = df["cosmo_rank"] * df["L_cosmo_s1.0"]


features = base_features + [
    "mass_metallicity", "dust_metallicity", "disp_mass_ratio", 
    "age_metallicity", "sqrt_Re_kpc", "BSD_likelihood", "cosmo_rank", 
    "cosmo_rank_L", *[f"L_cosmo_s{s}" for s in s_vals]
]


# Step 5: Train/Test Split and Scaling
X = df[features]
y = df[target]
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)


scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)


# Step 6: Model Training
# Random Forest
print("Training Random Forest...")
check_resources()
rf = RandomForestRegressor(n_estimators=100, max_depth=12, random_state=42, n_jobs=2)
rf.fit(X_train_scaled, y_train)
y_pred_rf = rf.predict(X_test_scaled)
r2_rf = r2_score(y_test, y_pred_rf)
mse_rf = mean_squared_error(y_test, y_pred_rf)


# Gradient Boosting
print("Training Gradient Boosting...")
check_resources()
gb = GradientBoostingRegressor(n_estimators=150, learning_rate=0.05, max_depth=6, random_state=42)
gb.fit(X_train_scaled, y_train)
y_pred_gb = gb.predict(X_test_scaled)
r2_gb = r2_score(y_test, y_pred_gb)
mse_gb = mean_squared_error(y_test, y_pred_gb)


print(f"Random Forest - R²: {r2_rf:.4f}, MSE: {mse_rf:.4f}")
print(f"Gradient Boosting - R²: {r2_gb:.4f}, MSE: {mse_gb:.4f}")


# Step 7: SHAP Analysis
print("Running SHAP for Random Forest...")
check_resources()
explainer_rf = shap.Explainer(rf, X_train_scaled)
shap_values_rf = explainer_rf(X_test_scaled[:500])
shap.summary_plot(shap_values_rf, X_test[:500], feature_names=features, plot_type="bar", show=True)
plt.title("SHAP Summary - Random Forest")
plt.tight_layout()
plt.savefig("shap_rf_summary.png")
plt.close()


print("Running SHAP for Gradient Boosting...")
check_resources()
explainer_gb = shap.Explainer(gb, X_train_scaled)
shap_values_gb = explainer_gb(X_test_scaled[:500])
shap.summary_plot(shap_values_gb, X_test[:500], feature_names=features, plot_type="bar", show=True)
plt.title("SHAP Summary - Gradient Boosting")
plt.tight_layout()
plt.savefig("shap_gb_summary.png")
plt.close()


# Step 8: PySR Symbolic Regression
print("Running PySR...")
cpu, mem = check_resources()
if mem > 75:
    print("Memory usage too high (>{}%). Skipping PySR.".format(75))
    y_pred_sym = np.zeros_like(y_test)
    r2_sym = 0.0
else:
    subsample_frac = 0.5
    X_train_sub = X_train.sample(frac=subsample_frac, random_state=42)
    y_train_sub = y_train.loc[X_train_sub.index]


    model = PySRRegressor(
        model_selection="best",
        niterations=10,
        binary_operators=["+", "-", "*", "/"],
        unary_operators=["exp", "log", "sqrt"],
        extra_sympy_mappings={"log": lambda x: np.log(np.abs(x) + 1e-5)},
        loss="loss(x, y) = (x - y)^2",
        maxsize=15,
        verbosity=1,
        random_state=42,
        procs=1
    )


    timeout = 15 * 60
    start_time = time.time()
    try:
        model.fit(X_train_sub, y_train_sub)
        y_pred_sym = model.predict(X_test)
        r2_sym = r2_score(y_test, y_pred_sym)
        print(f"PySR - R²: {r2_sym:.4f}")
        print("Top PySR Equations:\n", model.equations_.head())
    except Exception as e:
        if time.time() - start_time > timeout:
            print("PySR timed out after 15 minutes.")
        else:
            print(f"PySR failed: {e}")
        y_pred_sym = np.zeros_like(y_test)
        r2_sym = 0.0


# Step 9: Diagnostics
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
plt.show()
plt.close()


residuals = pd.DataFrame({
    "True": y_test,
    "RF": y_pred_rf - y_test,
    "GB": y_pred_gb - y_test,
    "PySR": y_pred_sym - y_test,
    "cosmo_rank": X_test["cosmo_rank"],
    "L_cosmo_s1": X_test["L_cosmo_s1.0"]
})
sns.scatterplot(data=residuals, x="True", y="RF", hue="cosmo_rank", size="L_cosmo_s1", alpha=0.6)
plt.axhline(0, color="black", linestyle="--")
plt.title("RF Residuals vs True log_SFR_Ha")
plt.savefig("residuals_rf.png")
plt.show()
plt.close()


print("Correlation of BSD Features with Residuals:")
print(residuals[["RF", "GB", "PySR", "cosmo_rank", "L_cosmo_s1"]].corr()[["RF", "GB", "PySR"]])


check_resources()
