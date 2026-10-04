# Rank option: weighted average (more influence to Pth100)
gz_df['cosmo_rank'] = 0.7 * gz_df['Pth100_norm'] + 0.3 * gz_df['morph_sum_norm']


# Ensure valid magnitude values before applying expected SFR formula
gz_df = gz_df[gz_df['dust_corrected_mag'].notna() & (gz_df['dust_corrected_mag'] < 100)]


# Compute expected SFR using a Kennicutt-Schmidt proxy and apply a log1p transformation
gz_df['expected_SFR'] = 1e-4 * (10 ** (0.4 * (22 - gz_df['dust_corrected_mag']))) ** 1.4
gz_df['expected_SFR'].replace([np.inf, -np.inf], np.nan, inplace=True)
gz_df.dropna(subset=['expected_SFR'], inplace=True)
gz_df['expected_SFR'] = np.log1p(gz_df['expected_SFR'])


# -------------------------------
# Step 5: Define features and target
# You can include cosmo_rank as an additional feature if desired.
X = gz_df[['z', 'rMag', 'Ar', 'Pth100', 'morph_sum', 'cosmo_rank']]
y = gz_df['expected_SFR']


# -------------------------------
# Step 6: Train-test split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)


# -------------------------------
# Step 7: Standardize features
scaler_std = StandardScaler()
X_train_scaled = scaler_std.fit_transform(X_train)
X_test_scaled = scaler_std.transform(X_test)


# -------------------------------
# Step 8: Random Forest - Optuna Optimization
check_system_resources()


def objective_rf(trial):
    model = RandomForestRegressor(
        max_depth=trial.suggest_int("max_depth", 5, 30),
        n_estimators=trial.suggest_int("n_estimators", 50, 500),
        min_samples_split=trial.suggest_int("min_samples_split", 2, 20),
        random_state=42,
        n_jobs=2
    )
    return np.mean(cross_val_score(model, X_train_scaled, y_train, cv=3, scoring='r2', n_jobs=2))


study_rf = optuna.create_study(direction="maximize")
study_rf.optimize(objective_rf, n_trials=50)


best_rf = RandomForestRegressor(**study_rf.best_params, random_state=42, n_jobs=2)
best_rf.fit(X_train_scaled, y_train)


# -------------------------------
# Step 9: Gradient Boosting - Optuna Optimization
def objective_gb(trial):
    model = GradientBoostingRegressor(
        max_depth=trial.suggest_int("max_depth", 3, 20),
        n_estimators=trial.suggest_int("n_estimators", 50, 500),
        min_samples_split=trial.suggest_int("min_samples_split", 2, 20),
        learning_rate=trial.suggest_float("learning_rate", 0.01, 0.3, log=True),
        random_state=42
    )
    return np.mean(cross_val_score(model, X_train_scaled, y_train, cv=3, scoring='r2', n_jobs=2))


study_gb = optuna.create_study(direction="maximize")
study_gb.optimize(objective_gb, n_trials=50)


best_gb = GradientBoostingRegressor(**study_gb.best_params, random_state=42)
best_gb.fit(X_train_scaled, y_train)


# -------------------------------
# Step 10: Evaluate Models
y_pred_rf = best_rf.predict(X_test_scaled)
y_pred_gb = best_gb.predict(X_test_scaled)


print(f"Random Forest - MSE: {mean_squared_error(y_test, y_pred_rf):.4f}, R²: {r2_score(y_test, y_pred_rf):.4f}")
print(f"Gradient Boosting - MSE: {mean_squared_error(y_test, y_pred_gb):.4f}, R²: {r2_score(y_test, y_pred_gb):.4f}")


# -------------------------------
# Step 11: SHAP Analysis and Saving Plots/Values
try:
    explainer_rf = shap.Explainer(best_rf, X_train_scaled)
    shap_values_rf = explainer_rf(X_test_scaled)
    shap.plots.beeswarm(shap_values_rf, show=False)
    plt.title("SHAP Summary - Random Forest")
    plt.savefig("shap_summary_rf.png")
    plt.close()
    pd.DataFrame(shap_values_rf.values, columns=X.columns).to_csv("shap_values_rf.csv", index=False)
except Exception as e:
    print(f"Random Forest SHAP analysis failed: {e}")


try:
    explainer_gb = shap.Explainer(best_gb, X_train_scaled)
    shap_values_gb = explainer_gb(X_test_scaled)
    shap.plots.beeswarm(shap_values_gb, show=False)
    plt.title("SHAP Summary - Gradient Boosting")
    plt.savefig("shap_summary_gb.png")
    plt.close()
    pd.DataFrame(shap_values_gb.values, columns=X.columns).to_csv("shap_values_gb.csv", index=False)
except Exception as e:
    print(f"Gradient Boosting SHAP analysis failed: {e}")


# -------------------------------
# Step 12: Symbolic Regression with PySR
try:
    symbolic_model = PySRRegressor(
        model_selection="best",
        niterations=500,
        population_size=2000,
        binary_operators=["+", "-", "*", "/"],
        unary_operators=["sqrt", "log", "exp", "sin", "cos"],
        loss="loss(x, y) = (x - y)^2",
        maxsize=30,
        verbosity=1,
        procs=4,
        random_state=42
    )
    symbolic_model.fit(X_train_scaled, y_train)
    print("Best symbolic models:\n", symbolic_model)
    
    y_pysr_pred = symbolic_model.predict(X_test_scaled)
    print(f"PySR R² score: {r2_score(y_test, y_pysr_pred):.4f}")
    
    # Export the symbolic model's equations
    symbolic_model.equations_.to_csv("pysr_equations.csv", index=False)
    print("Top PySR Equations:\n", symbolic_model.equations_.head())
except Exception as e:
    print(f"Symbolic regression failed: {e}")


# -------------------------------
# Step 13: Visual Comparison of R² Scores
try:
    model_names = []
    r2_scores = []
    if best_rf is not None:
        model_names.append("Random Forest")
        r2_scores.append(r2_score(y_test, y_pred_rf))
    if best_gb is not None:
        model_names.append("Gradient Boosting")
        r2_scores.append(r2_score(y_test, y_pred_gb))
    if 'y_pysr_pred' in locals():
        model_names.append("PySR")
        r2_scores.append(r2_score(y_test, y_pysr_pred))
    
    if model_names:
        plt.bar(model_names, r2_scores, color=['skyblue', 'salmon', 'limegreen'][:len(model_names)])
        plt.ylabel("R² Score")
        plt.title("Model Performance Comparison")
        plt.ylim(0, 1)
        plt.savefig("model_comparison_r2.png")
        plt.close()
except Exception as e:
    print(f"Model comparison plot failed: {e}")


# -------------------------------
# Final system resource check
check_system_resources()
