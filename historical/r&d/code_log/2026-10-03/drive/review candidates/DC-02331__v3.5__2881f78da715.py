    real2_y = np.zeros(len(real2))


# Ensure real1_y is also defined if you plan to evaluate on both catalogs
if 'real1' in locals():
    real1_y = real1['rank'] if 'rank' in real1.columns else np.zeros(len(real1))


print(f" -> Evaluation target 'real2_y' ready. Shape: {real2_y.shape}")


# ====================== OPTUNA EXECUTION ======================
print("\n Running Multi-Objective Optuna (MSE + (1-R²) + W₂)...")
# Now that synth_y exists, the objective function won't crash
study = optuna.create_study(direction='minimize')
study.optimize(objective, n_trials=int(15))


# ====================== MULTI-OBJECTIVE OPTUNA WITH WASSERSTEIN ======================
def objective(trial):
    param = {
        'n_estimators': int(trial.suggest_int('n_estimators', 400, 800)),
        'learning_rate': float(trial.suggest_float('learning_rate', 0.01, 0.05)),
        'max_depth': int(trial.suggest_int('max_depth', 4, 7)),
        'subsample': float(trial.suggest_float('subsample', 0.6, 0.95)),
        'random_state': 42
    }
    kf = KFold(n_splits=int(5), shuffle=True, random_state=int(42))
    mse_scores, r2_scores, w2_scores = [], [], []
    
    for tr, val in kf.split(synth):
        X_train, y_train = synth[common_features].iloc[tr], synth_y.iloc[tr]
        X_val, y_val = synth[common_features].iloc[val], synth_y.iloc[val]
        
        model = xgb.XGBRegressor(**param)
        model.fit(X_train, y_train)
        preds = model.predict(X_val)
        
        mse_scores.append(mean_squared_error(y_val, preds))
        r2_scores.append(r2_score(y_val, preds))
        w2_scores.append(wasserstein_distance(y_val, preds))
    
    composite_loss = np.mean(mse_scores) + (1.0 - np.mean(r2_scores)) + (2.0 * np.mean(w2_scores))
    return composite_loss


print("\n Running Multi-Objective Optuna (MSE + (1-R²) + W₂)...")
study = optuna.create_study(direction='minimize')
study.optimize(objective, n_trials=int(15))
best_params = study.best_params
print(f"Best parameters: {best_params}")


# ====================== FULL ECC STRATIFIED STACKING ======================
class StableECCStacker:
    def __init__(self, params):
        from sklearn.linear_model import Lasso, Ridge
        self.base_models = [
            ('xgb', xgb.XGBRegressor(**params)),
            ('lgb', lgb.LGBMRegressor(n_estimators=int(400), verbose=int(-1))),
            ('cat', cb.CatBoostRegressor(iterations=int(400), verbose=int(0)))
