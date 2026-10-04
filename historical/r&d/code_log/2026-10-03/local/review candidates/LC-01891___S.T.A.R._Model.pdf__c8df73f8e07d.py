# Optuna optimization for Gradient Boosting
def objective_gb(trial):
    params = {
        'n_estimators': trial.suggest_int('n_estimators', 100, 500),
        'learning_rate': trial.suggest_float('learning_rate', 0.01, 0.2, log=True),
        'max_depth': trial.suggest_int('max_depth', 3, 10),
        'random_state': 42
    }
    model = GradientBoostingRegressor(**params)
    cv = KFold(n_splits=5, shuffle=True, random_state=42)
    scores = cross_val_score(model, X_train_scaled, y_train, cv=cv, scoring='r2', n_jobs=2)
    return scores.mean()

study_gb = optuna.create_study(direction='maximize')
study_gb.optimize(objective_gb, n_trials=20)
best_params_gb = study_gb.best_params
print("Best Gradient Boosting Parameters:", best_params_gb)
print("Best Gradient Boosting CV R²:", study_gb.best_value)

# Train Gradient Boosting with best parameters
gb = GradientBoostingRegressor(**best_params_gb, random_state=42)
gb.fit(X_train_scaled, y_train)
y_pred_gb = gb.predict(X_test_scaled)
r2_gb = r2_score(y_test, y_pred_gb)

# Cross-validation for final GB model
cv_scores_gb = cross_val_score(gb, X_train_scaled, y_train, cv=5, scoring='r2', n_jobs=2)