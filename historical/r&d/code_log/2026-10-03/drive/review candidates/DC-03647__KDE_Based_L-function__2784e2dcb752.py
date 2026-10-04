def objective_rf(trial):
    params = {
        "max_depth": trial.suggest_int("max_depth", 5, 20),
        "n_estimators": trial.suggest_int("n_estimators", 50, 250),
        "min_samples_split": trial.suggest_int("min_samples_split", 2, 20)
    }
    model = RandomForestRegressor(**params, random_state=42, n_jobs=1)  # safer n_jobs
    
    scores = cross_val_score(model, X_train_scaled, y_train, cv=3, scoring='r2', n_jobs=1)  # safer parallel
    return scores.mean()
