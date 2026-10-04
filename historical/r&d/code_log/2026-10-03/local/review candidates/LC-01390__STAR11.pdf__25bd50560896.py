X = X.replace([np.inf, -np.inf], np.nan).fillna(X.median(skipna=True))
y = y.replace([np.inf, -np.inf], np.nan).fillna(y.median(skipna=True))
print(f"Rows after X and y imputation: {len(X)}")

# Train/test split
=========================================================================================
==============================================================================
if len(X) < 10:
    raise ValueError(f"Only {len(X)} rows after cleaning. Check data preprocessing.")
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# Verify inputs
=========================================================================================
=================================================================================
print("NaN in X_train_scaled:", np.isnan(X_train_scaled).sum())
print("Inf in X_train_scaled:", np.isinf(X_train_scaled).sum())
print("NaN in y_train:", y_train.isna().sum())
print("Inf in y_train:", np.isinf(y_train).sum())
print("Feature selection and scaling complete. Initiating *S.T.A.R. training with Optuna...")

# Optuna Optimizations
=========================================================================================
==========================================================================
def objective_hgb(trial):
    params = {
        'max_iter': trial.suggest_int('max_iter', 100, 500),
        'max_depth': trial.suggest_int('max_depth', 3, 10),
        'learning_rate': trial.suggest_float('learning_rate', 0.01, 0.2, log=True),
        'l2_regularization': trial.suggest_float('l2_regularization', 0.1, 10.0),
        'max_leaf_nodes': trial.suggest_int('max_leaf_nodes', 20, 50),
        'min_samples_leaf': trial.suggest_int('min_samples_leaf', 10, 30),
        'random_state': 42
    }
    model = HistGradientBoostingRegressor(**params)
    cv = KFold(n_splits=5, shuffle=True, random_state=42)
    scores = cross_val_score(model, X_train_scaled, y_train, cv=cv, scoring='r2')
    mean_score = np.nanmean(scores)
    if np.isnan(mean_score):
        print(f"HGB Trial {trial.number} failed: scores = {scores}")
    return mean_score if not np.isnan(mean_score) else -np.inf

def objective_lgb(trial):