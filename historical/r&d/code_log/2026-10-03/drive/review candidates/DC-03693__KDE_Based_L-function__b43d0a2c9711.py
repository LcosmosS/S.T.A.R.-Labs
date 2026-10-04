def objective_rf(trial):
    model = RandomForestRegressor(
        max_depth=trial.suggest_int("max_depth", 5, 30),
        n_estimators=trial.suggest_int("n_estimators", 50, 500),
        min_samples_split=trial.suggest_int("min_samples_split", 2, 20),
        random_state=42,
        n_jobs=2  # Change to a lower number of parallel jobs
    )
    return np.mean(cross_val_score(model, X_train_scaled, y_train, cv=3, scoring='r2', n_jobs=2))  # Use n_jobs=2


study_rf = optuna.create_study(direction="maximize")
study_rf.optimize(objective_rf, n_trials=50)


best_rf = RandomForestRegressor(**study_rf.best_params, random_state=42, n_jobs=2)  # Adjust n_jobs here as well
best_rf.fit(X_train_scaled, y_train)


# -------------------------------


# After fitting, explicitly clear unused memory
import gc
gc.collect()
