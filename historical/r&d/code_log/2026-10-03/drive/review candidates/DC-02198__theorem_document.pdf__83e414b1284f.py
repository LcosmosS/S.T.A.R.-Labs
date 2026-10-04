max_depth=trial.suggest_int("max_depth", 3, 20), \n
n_estimators=trial.suggest_int("n_estimators", 50, 500), \n
min_samples_split=trial.suggest_int("min_samples_split", 2, 20), \n
learning_rate=trial.suggest_float("learning_rate", 0.01, 0.3, log=True), \n
random_state=42 \n ) \n return np.mean(cross_val_score(model, X_train_scaled,
y_train, cv=3, scoring=\'r2\', \nn_jobs=2)) \n \n study_gb =
optuna.create_study(direction="maximize") \n study_gb.optimize(objective_gb,
n_trials=50) \n \n best_gb = GradientBoostingRegressor(**study_gb.best_params,
random_state=42) \n best_gb.fit(X_train_scaled, y_train) \nexcept Exception as e: \n
print(f"Gradient Boosting training failed: {e}") \n \n# ------------------------------- \n#
Step 8: Evaluate Models \nif best_rf is not None: \n\n y_pred_rf =
best_rf.predict(X_test_scaled) \n print(f"Random Forest - MSE:
