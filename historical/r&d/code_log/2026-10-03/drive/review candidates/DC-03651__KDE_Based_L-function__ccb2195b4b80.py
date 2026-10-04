def objective_rf(trial):
    max_depth = trial.suggest_int("max_depth", 3, 15)
    n_estimators = trial.suggest_int("n_estimators", 50, 300)
    min_samples_split = trial.suggest_int("min_samples_split", 2, 10)


    model = RandomForestRegressor(
        max_depth=max_depth,
        n_estimators=n_estimators,
        min_samples_split=min_samples_split,
        random_state=42,
        n_jobs=-1  # this is okay as long as cross_val_score uses n_jobs=1
    )


    scores = cross_val_score(model, X_train_scaled, y_train, cv=3, scoring='r2', n_jobs=1)
    return scores.mean()
