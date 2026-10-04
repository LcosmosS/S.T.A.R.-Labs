def objective_gb(trial):
    ### DIAGNOSTIC BLOCK: Check training data integrity ###
    print("\n[DIAGNOSTIC] Checking X_train_scaled and y_train:")
    print("X_train_scaled sample:\n", pd.DataFrame(X_train_scaled).head())
    print("X_train_scaled - min:", np.min(X_train_scaled), " max:", np.max(X_train_scaled), " NaNs:", np.isnan(X_train_scaled).any())
    print("y_train sample:\n", y_train.head())
    print("y_train - min:", y_train.min(), " max:", y_train.max(), " NaNs:", y_train.isna().any())


    model = GradientBoostingRegressor(
        max_depth=trial.suggest_int("max_depth", 3, 20),
        n_estimators=trial.suggest_int("n_estimators", 50, 500),
        min_samples_split=trial.suggest_int("min_samples_split", 2, 20),
        learning_rate=trial.suggest_float("learning_rate", 0.01, 0.3, log=True),
        random_state=42
    )
    return np.mean(cross_val_score(model, X_train_scaled, y_train, cv=3, scoring='r2', n_jobs=-1))
