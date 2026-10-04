        print(f"R^2 Score (LightGBM, Test): {r2_lgb:.4f}")
    elif model_name == 'XGBoost':
        study_xgb.optimize(objective_xgb, n_trials=20)
        print(f"Best XGBoost Parameters: {study_xgb.best_params}")
        print(f"Best XGBoost CV R²: {study_xgb.best_value:.4f}")
        xgb_model.set_params(**study_xgb.best_params)
        xgb_model.fit(X_train_scaled, y_train)
        y_pred_xgb = xgb_model.predict(X_test_scaled)
        r2_xgb = r2_score(y_test, y_pred_xgb)
        cv_scores_xgb = cross_val_score(xgb_model, X_train_scaled, y_train, cv=5, scoring='r2')
        print(f"XGBoost 5-Fold CV R²: Mean = {cv_scores_xgb.mean():.4f}, Std =
