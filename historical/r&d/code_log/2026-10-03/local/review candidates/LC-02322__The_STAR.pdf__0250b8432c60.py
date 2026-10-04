desc="Training Models"):
    print(f"Training {model_name}...")
    if model_name == 'HistGradientBoosting':
        study_hgb.optimize(objective_hgb, n_trials=20)
        print(f"Best HistGradientBoosting Parameters: {study_hgb.best_params}")
        print(f"Best HistGradientBoosting CV R²: {study_hgb.best_value:.4f}")
        hgb.set_params(**study_hgb.best_params)
        hgb.fit(X_train_scaled, y_train)
        y_pred_hgb = hgb.predict(X_test_scaled)
        r2_hgb = r2_score(y_test, y_pred_hgb)
        cv_scores_hgb = cross_val_score(hgb, X_train_scaled, y_train, cv=5, scoring='r2')
        print(f"HistGradientBoosting 5-Fold CV R²: Mean = {cv_scores_hgb.mean():.4f}, Std =
