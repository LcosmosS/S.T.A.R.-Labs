X = df[features] y = df[target]
# Train/test split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
# Normalize features
scaler = StandardScaler() X_train_scaled = scaler.fit_transform(X_train) X_test_scaled = scaler.transform(X_test)
# Optuna optimization for Random Forest
def objective_rf(trial): params = { 'n_estimators': trial.suggest_int('n_estimators', 100, 500), 'max_depth': trial.suggest_int('max_depth', 5, 20), 'min_samples_split': trial.suggest_int('min_samples_split', 2, 10), 'random_state': 42 } model = RandomForestRegressor(**params) cv = KFold(n_splits=5, shuffle=True, random_state=42) scores = cross_val_score(model, X_train_scaled, y_train, cv=cv, scoring='r2') return scores.mean()
study_rf = optuna.create_study(direction='maximize') study_rf.optimize(objective_rf, n_trials=20) best_params_rf = study_rf.best_params print("Best Random Forest Parameters:", best_params_rf) print("Best Random Forest CV R²:", study_rf.best_value)
# Train Random Forest with best parameters
rf = RandomForestRegressor(**best_params_rf, random_state=42) rf.fit(X_train_scaled, y_train) y_pred_rf = rf.predict(X_test_scaled) r2_rf = r2_score(y_test, y_pred_rf)
# Cross-validation for final RF model
cv_scores_rf = cross_val_score(rf, X_train_scaled, y_train, cv=5, scoring='r2') print(f"Random Forest 5-Fold CV R²: Mean = {cv_scores_rf.mean():.4f}, Std = {cv_scores_rf.std():.4f}")
# Optuna optimization for Gradient Boosting
def objective_gb(trial): params = { 'n_estimators': trial.suggest_int('n_estimators', 100, 500), 'learning_rate': trial.suggest_float('learning_rate', 0.01, 0.2, log=True), 'max_depth': trial.suggest_int('max_depth', 3, 10), 'random_state': 42 } model = GradientBoostingRegressor(**params) cv = KFold(n_splits=5, shuffle=True, random_state=42) scores = cross_val_score(model, X_train_scaled, y_train, cv=cv, scoring='r2') return scores.mean()
study_gb = optuna.create_study(direction='maximize') study_gb.optimize(objective_gb, n_trials=20) best_params_gb = study_gb.best_params print("Best Gradient Boosting Parameters:", best_params_gb) print("Best Gradient Boosting CV R²:", study_gb.best_value)
# Train Gradient Boosting with best parameters
gb = GradientBoostingRegressor(**best_params_gb, random_state=42) gb.fit(X_train_scaled, y_train) y_pred_gb = gb.predict(X_test_scaled) r2_gb = r2_score(y_test, y_pred_gb)
# Cross-validation for final GB model
cv_scores_gb = cross_val_score(gb, X_train_scaled, y_train, cv=5, scoring='r2') print(f"Gradient Boosting 5-Fold CV R²: Mean = {cv_scores_gb.mean():.4f}, Std = {cv_scores_gb.std():.4f}")
print(f"R^2 Score (Random Forest, Test Set): {r2_rf:.4f}") print(f"R^2 Score (Gradient Boosting, Test Set): {r2_gb:.4f}")
# SHAP for feature selection
explainer_rf = shap.Explainer(rf, X_train_scaled) shap_values_rf = explainer_rf(X_test_scaled) explainer_gb = shap.Explainer(gb, X_train_scaled) shap_values_gb = explainer_gb(X_test_scaled) shap.summary_plot(shap_values_rf, X_test_scaled, plot_type="bar", show=False) plt.title("SHAP Summary - Random Forest") plt.tight_layout() plt.savefig("shap_rf_summary.png") plt.clf() shap.summary_plot(shap_values_gb, X_test_scaled, plot_type="bar", show=False) plt.title("SHAP Summary - Gradient Boosting") plt.tight_layout() plt.savefig("shap_gb_summary.png") plt.clf()
# Feature selection based on SHAP
shap_values_rf_mean = np.abs(shap_values_rf.values).mean(axis=0) feature_importance = pd.DataFrame({"feature": features, "importance": shap_values_rf_mean}) feature_importance = feature_importance.sort_values("importance", ascending=False) top_features = feature_importance["feature"].head(10).tolist() bsd_features = ["cosmo_rank", "L_cosmo_s_1.0", "cosmo_rank_L", "cosmo_rank_scaled", "L_cosmo_s1_scaled", "cosmo_rank_L_mass", "L_cosmo_s1_metallicity"] for bsd_feature in bsd_features: if bsd_feature not in top_features: top_features.append(bsd_feature) X_selected = df[top_features] X_train_selected, X_test_selected, _, _ = train_test_split(X_selected, y, test_size=0.2, random_state=42) X_train_selected_scaled = scaler.fit_transform(X_train_selected) X_test_selected_scaled = scaler.transform(X_test_selected)
# Symbolic Regression with gplearn
symbolic_model = SymbolicRegressor( population_size=3000, generations=150, stopping_criteria=0.01, p_crossover=0.7, p_subtree_mutation=0.1, p_hoist_mutation=0.05, p_point_mutation=0.1, max_samples=0.9, verbose=1, parsimony_coefficient=0.0001, random_state=42, function_set=('add', 'sub', 'mul', 'div', 'sqrt', 'log', 'sin', 'cos') ) symbolic_model.fit(X_train_selected_scaled, y_train) y_pred_sym = symbolic_model.predict(X_test_selected_scaled) r2_sym = r2_score(y_test, y_pred_sym) print(f"gplearn R²: {r2_sym:.4f}") print("Symbolic Expression:") print(symbolic_model._program)
# Cross-validation for symbolic model
cv_scores_sym = cross_val_score(symbolic_model, X_train_selected_scaled, y_train, cv=5, scoring='r2') print(f"Symbolic Regression 5-Fold CV R²: Mean = {cv_scores_sym.mean():.4f}, Std = {cv_scores_sym.std():.4f}")
# Save symbolic expression as polynomial fit plot and print the equation
x = np.linspace(min(y_test), max(y_test), 500) y_expr = symbolic_model.predict(scaler.transform(np.tile(X_test_selected.mean().values, (500,1)))) p = Polynomial.fit(y_test, y_pred_sym, deg=3)
# Extract polynomial coefficients
coeffs = p.coef print("Polynomial Fit Equation (degree 3):") print(f"y = {coeffs[0]:.4f} + {coeffs[1]:.4f}*x + {coeffs[2]:.4f}*x^2 + {coeffs[3]:.4f}*x^3")
# Plot the polynomial fit
plt.plot(*p.linspace(), label="Polynomial Fit") plt.scatter(y_test, y_pred_sym, s=10, alpha=0.5, label="Symbolic Predictions") plt.xlabel("True log_SFR_Ha") plt.ylabel("Predicted log_SFR_Ha") plt.title("Symbolic Regression Fit with Polynomial") plt.legend() plt.tight_layout() plt.savefig("gplearn_expression_plot.png") plt.clf()
# Plot predictions vs true
plt.scatter(y_test, y_pred_rf, alpha=0.5, label="RF", marker="o") plt.scatter(y_test, y_pred_gb, alpha=0.5, label="GB", marker="s") plt.scatter(y_test, y_pred_sym, alpha=0.5, label="Symbolic", marker="^") plt.plot([y.min(), y.max()], [y.min(), y.max()], "k--") plt.xlabel("True log_SFR_Ha") plt.ylabel("Predicted") plt.title("Model Predictions vs True Values") plt.legend() plt.tight_layout() plt.savefig("model_comparison.png") plt.clf()
# Residuals and Correlation Analysis
residuals = pd.DataFrame({ "True": y_test, "RF": y_pred_rf - y_test, "GB": y_pred_gb - y_test, "Symbolic": y_pred_sym - y_test, "cosmo_rank": X_test["cosmo_rank"], "L_cosmo_s1": X_test["L_cosmo_s_1.0"] }) sns.scatterplot(data=residuals, x="True", y="Symbolic", hue="cosmo_rank", size="L_cosmo_s1", alpha=0.6) plt.axhline(0, color="black", linestyle="--") plt.title("Symbolic Residuals vs True log_SFR_Ha") plt.savefig("residuals_sym.png") plt.clf()
print("Correlation of BSD Features with Residuals:") print(residuals[["RF", "GB", "Symbolic", "cosmo_rank", "L_cosmo_s1"]].corr()[["RF", "GB", "Symbolic"]])
