def objective(trial):
   params = {
       "n_estimators": trial.suggest_int("n_estimators", 100, 1000),
       "max_depth": trial.suggest_int("max_depth", 4, 12),
       "learning_rate": trial.suggest_float("learning_rate", 0.01, 0.2),
       "subsample": trial.suggest_float("subsample", 0.7, 1.0),
       "reg_alpha": trial.suggest_float("reg_alpha", 0.0, 1.0),
       "reg_lambda": trial.suggest_float("reg_lambda", 0.0, 1.0),
   }
   model = XGBRegressor(**params)
   model.fit(X_train, y_train)
   preds = model.predict(X_test)
   return 1 - mean_absolute_error(y_test, preds)

study = optuna.create_study(direction="maximize")
study.optimize(objective, n_trials=50)

best_params = study.best_params
optuna_model = XGBRegressor(**best_params)
optuna_model.fit(X_train, y_train)
optuna_preds = optuna_model.predict(X_test)
results["Optuna_XGBoost"] = {
   "R2": r2_score(y_test, optuna_preds),
   "MAE": mean_absolute_error(y_test, optuna_preds)
}
