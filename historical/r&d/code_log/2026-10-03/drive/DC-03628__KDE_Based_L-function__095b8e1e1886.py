def objective_rf(trial):
    max_depth = trial.suggest_int("max_depth", 5, 30)
    n_estimators = trial.suggest_int("n_estimators", 50, 500)
    min_samples_split = trial.suggest_int("min_samples_split", 2, 20)
    
    model = RandomForestRegressor(
        max_depth=max_depth,
        n_estimators=n_estimators,
        min_samples_split=min_samples_split,
        random_state=42,
        n_jobs=1  # <--- Only 1 thread per trial
    )
    
    scores = cross_val_score(model, X_train_scaled, y_train, cv=3, scoring='r2', n_jobs=1)  # <--- Also 1 thread
    return np.mean(scores)
