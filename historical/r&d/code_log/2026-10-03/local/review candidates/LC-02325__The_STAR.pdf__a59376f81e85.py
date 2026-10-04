        print(f"R^2 Score (XGBoost, Test): {r2_xgb:.4f}")
    elif model_name == 'CatBoost':
        study_cat.optimize(objective_cat, n_trials=20)
        print(f"Best CatBoost Parameters: {study_cat.best_params}")
        print(f"Best CatBoost CV R²: {study_cat.best_value:.4f}")
        cat_model.set_params(**study_cat.best_params)
        cat_model.fit(X_train_scaled, y_train)
        y_pred_cat = cat_model.predict(X_test_scaled)
        r2_cat = r2_score(y_test, y_pred_cat)
        cv_scores_cat = cross_val_score(cat_model, X_train_scaled, y_train, cv=5, scoring='r2')
        print(f"CatBoost 5-Fold CV R²: Mean = {cv_scores_cat.mean():.4f}, Std =
