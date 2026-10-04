    if cols_to_impute:
        df[cols_to_impute] = imputer.fit_transform(df[cols_to_impute])
        print(f"   {name} — {len(cols_to_impute)} columns imputed with KNN")


# ====================== DATASET-SPECIFIC FEATURE COLS ======================
synth_feature_cols = base_cols + ['synth_local_betti_2']
real1_feature_cols = base_cols + ['real1_local_betti_2']
real2_feature_cols = base_cols + ['real2_local_betti_2']


# Targets
synth_y = synth['exact_rank']
real1_y = real1['real1_local_betti_1']
real2_y = real2['real2_local_betti_1']


# ====================== OPTUNA ON SYNTHETIC ONLY ======================
def objective(trial):
    params = {
        'n_estimators': trial.suggest_int('n_estimators', 200, 800),
        'learning_rate': trial.suggest_float('learning_rate', 0.005, 0.08, log=True),
        'max_depth': trial.suggest_int('max_depth', 3, 7),
        'subsample': trial.suggest_float('subsample', 0.6, 0.95),
        'colsample_bytree': trial.suggest_float('colsample_bytree', 0.6, 0.95),
        'reg_alpha': trial.suggest_float('reg_alpha', 1e-4, 5.0, log=True),
        'reg_lambda': trial.suggest_float('reg_lambda', 1e-4, 5.0, log=True),
        'random_state': 42
    }
    kf = KFold(n_splits=5, shuffle=True, random_state=42)
    scores = []
    X = synth[synth_feature_cols].copy()
    y = synth_y
    for tr, val in kf.split(X):
        model = xgb.XGBRegressor(**params)
        model.fit(X.iloc[tr], y.iloc[tr])
        preds = model.predict(X.iloc[val])
        scores.append(r2_score(y.iloc[val], preds))
    return np.mean(scores)


print("\n🔧 Running Optuna on synthetic (strict control)...")
study = optuna.create_study(direction='maximize')
study.optimize(objective, n_trials=30)
best_params = study.best_params
print(f"✅ Best base params: {best_params}")


# ====================== PySR INJECTION ======================
from pysr import PySRRegressor
pysr = PySRRegressor(niterations=80, maxsize=12, random_state=42)
pysr.fit(synth[synth_feature_cols], synth_y)


synth['pysr_symbolic'] = pysr.predict(synth[synth_feature_cols])
real1['pysr_symbolic'] = pysr.predict(real1[real1_feature_cols])
real2['pysr_symbolic'] = pysr.predict(real2[real2_feature_cols])


synth_feature_cols.append('pysr_symbolic')
real1_feature_cols.append('pysr_symbolic')
real2_feature_cols.append('pysr_symbolic')


# ====================== EXPANDED STACKING ======================
def run_stacked_cv(df, y, name, feature_list):
    X = df[feature_list].copy()
    kf = KFold(n_splits=5, shuffle=True, random_state=42)
    r2_list, mse_list = [], []
    for tr_idx, val_idx in kf.split(X):
        X_tr, X_val = X.iloc[tr_idx], X.iloc[val_idx]
        y_tr, y_val = y.iloc[tr_idx], y.iloc[val_idx]
        xgb_m = xgb.XGBRegressor(**best_params)
        lgb_m = lgb.LGBMRegressor(n_estimators=400, learning_rate=0.03, max_depth=5, random_state=42)
        cat_m = cb.CatBoostRegressor(iterations=400, learning_rate=0.03, depth=5, random_state=42, verbose=0)
        hist_m = HistGradientBoostingRegressor(max_iter=400, learning_rate=0.03, max_depth=5, random_state=42)
        svr_m = SVR(kernel='rbf', C=1.0, epsilon=0.1)
        
        xgb_m.fit(X_tr, y_tr)
        lgb_m.fit(X_tr, y_tr)
        cat_m.fit(X_tr, y_tr)
        hist_m.fit(X_tr, y_tr)
        svr_m.fit(X_tr, y_tr)
        
        stack_tr = np.column_stack((xgb_m.predict(X_tr), lgb_m.predict(X_tr), cat_m.predict(X_tr),
                                    hist_m.predict(X_tr), svr_m.predict(X_tr), pysr.predict(X_tr)))
        stack_val = np.column_stack((xgb_m.predict(X_val), lgb_m.predict(X_val), cat_m.predict(X_val),
                                     hist_m.predict(X_val), svr_m.predict(X_val), pysr.predict(X_val)))
        
        meta = Ridge(alpha=1.0)
        meta.fit(stack_tr, y_tr)
        y_pred = meta.predict(stack_val)
        
        r2_list.append(r2_score(y_val, y_pred))
        mse_list.append(mean_squared_error(y_val, y_pred))
    print(f"\n{name} — 5-Fold Expanded Stacked CV")
    print(f"   R²  = {np.mean(r2_list):.4f} ± {np.std(r2_list):.4f}")
    print(f"   MSE = {np.mean(mse_list):.4f} ± {np.std(mse_list):.4f}")
    return np.mean(r2_list), np.mean(mse_list)


print("\nRunning expanded stacked CV...")
r2_synth, _ = run_stacked_cv(synth, synth_y, "Synthetic", synth_feature_cols)
r2_real1, _ = run_stacked_cv(real1, real1_y, "Real1 JApJ", real1_feature_cols)
r2_real2, _ = run_stacked_cv(real2, real2_y, "Real2 DESI/SDSS", real2_feature_cols)


print("\n🎉 Step 19 Complete — KNN Imputation + Expanded Stacking")
print("Reply with **analyze step 19** for full interpretation, tables, and conclusions.")
