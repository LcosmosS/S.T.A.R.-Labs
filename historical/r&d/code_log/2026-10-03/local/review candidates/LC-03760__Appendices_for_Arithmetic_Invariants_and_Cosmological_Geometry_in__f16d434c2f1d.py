    denom_y = y.denominator() if hasattr(y, 'denominator') else 1
    factors_x = factor(denom_x) if denom_x != 1 else []
    if len(factors_x) == 1 and len(factors_x[0][0].prime_factors()) == 1:
        return {'type': 'Recursive', 'structure': 'power_of_prime'}
    return {'type': 'Recursive', 'structure': 'other_sequence'}

# --- 13. Preprocess Clustering Features ---
def preprocess_clustering_features(X_struct, feature_cols):
    log_function("preprocess_clustering_features")
    X_struct = X_struct.copy()
    imputer = KNNImputer(n_neighbors=5, weights='distance')
    X_struct[feature_cols] = imputer.fit_transform(X_struct[feature_cols])
    print(f"preprocess_clustering_features: Imputed NaN in {feature_cols}")
    return X_struct

# --- 14. Hyperparameter Optimization ---
def optimize_catboost_classifier(X, y, n_trials=50):
    log_function("optimize_catboost_classifier")
    if CatBoostClassifier is None or create_study is None:
        print("CatBoost or Optuna not installed. Skipping optimization.")
        return None
    def objective(trial):
        params = {
            'iterations': trial.suggest_int('iterations', 100, 1000),
            'depth': trial.suggest_int('depth', 4, 10),
            'learning_rate': trial.suggest_float('learning_rate', 0.01, 0.3,
log=True),
            'l2_leaf_reg': trial.suggest_float('l2_leaf_reg', 1, 10)
        }
        model = CatBoostClassifier(**params, verbose=0)
        return cross_val_score(model, X, y, cv=5).mean()
    study = create_study(direction='maximize')
    study.optimize(objective, n_trials=n_trials)
    return study.best_params

def optimize_catboost_regressor(X, y, n_trials=50):
    log_function("optimize_catboost_regressor")
    if CatBoostRegressor is None or create_study is None:
        print("CatBoost or Optuna not installed. Skipping optimization.")
        return None
    def objective(trial):
        params = {
            'iterations': trial.suggest_int('iterations', 100, 1000),
            'depth': trial.suggest_int('depth', 4, 10),
            'learning_rate': trial.suggest_float('learning_rate', 0.01, 0.3,
log=True),
            'l2_leaf_reg': trial.suggest_float('l2_leaf_reg', 1, 10)
        }
        model = CatBoostRegressor(**params, verbose=0)
        return cross_val_score(model, X, y, cv=5, scoring='r2').mean()
    study = create_study(direction='maximize')
    study.optimize(objective, n_trials=n_trials)
