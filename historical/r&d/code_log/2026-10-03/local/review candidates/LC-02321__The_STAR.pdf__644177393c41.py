    model = xgb.XGBRegressor(**params)
    cv = KFold(n_splits=5, shuffle=True, random_state=42)
    scores = cross_val_score(model, X_train_scaled, y_train, cv=cv, scoring='r2')
    mean_score = np.nanmean(scores)
    if np.isnan(mean_score):
        print(f"XGB Trial {trial.number} failed: scores = {scores}")
    return mean_score if not np.isnan(mean_score) else -np.inf

def objective_cat(trial):
    params = {
        'iterations': trial.suggest_int('iterations', 100, 500),
        'depth': trial.suggest_int('depth', 4, 10),
        'learning_rate': trial.suggest_float('learning_rate', 0.01, 0.2, log=True),
        'l2_leaf_reg': trial.suggest_float('l2_leaf_reg', 1, 10),
        'random_seed': 42,
        'verbose': 0
    }
    model = CatBoostRegressor(**params)
    cv = KFold(n_splits=5, shuffle=True, random_state=42)
    scores = cross_val_score(model, X_train_scaled, y_train, cv=cv, scoring='r2')
    mean_score = np.nanmean(scores)
    if np.isnan(mean_score):
        print(f"Cat Trial {trial.number} failed: scores = {scores}")
    return mean_score if not np.isnan(mean_score) else -np.inf

# Define models and studies
========================================================================
========================================================================
==============
hgb = HistGradientBoostingRegressor(random_state=42, n_jobs=2)
symbolic_reg = SymbolicRegressor(population_size=1000, generations=20, random_state=42,
n_jobs=2)
lgb_model = lgb.LGBMRegressor(random_state=42, verbose=-1)
xgb_model = xgb.XGBRegressor(random_state=42)
cat_model = CatBoostRegressor(random_seed=42, verbose=0)

study_hgb = optuna.create_study(direction='maximize')
study_lgb = optuna.create_study(direction='maximize')
study_xgb = optuna.create_study(direction='maximize')
study_cat = optuna.create_study(direction='maximize')

print("Initiating *S.T.A.R. calculations...")