def add_thesis_features(df): ...  # (your exact function from previous steps — unchanged)


synth = add_thesis_features(synth)
real1 = add_thesis_features(real1)
real2 = add_thesis_features(real2)


# Fixed physical topology with Betti_2 (from Step 18)
def add_physical_local_topology(df, name, ra_col, de_col, z_col, k=25): ...  # (your corrected version — unchanged)


print("\nComputing topology...")
real1, _ = add_physical_local_topology(real1, "real1", "RAJ2000", "DEJ2000", "Vcmb")
real2, _ = add_physical_local_topology(real2, "real2", "RAdeg", "DEdeg", "zphot")
synth, _ = add_physical_local_topology(synth, "synth", "synthetic_RA", "synthetic_DE", "synthetic_z")


feature_cols = ['flux_gr', 'pm_mag_proxy', 'mag_ratio', 'T_cosmo', 'Tully_Fisher', 'Anthropic',
                'real1_local_betti_2', 'real2_local_betti_2', 'synth_local_betti_2']


# Targets
synth_y = synth['exact_rank']
real1_y = real1['real1_local_betti_1']
real2_y = real2['real2_local_betti_1']


# Optuna on synthetic only (unchanged)
def objective(trial): ...  # (your Optuna function from Step 18)


print("\n🔧 Running Optuna on synthetic...")
study = optuna.create_study(direction='maximize')
study.optimize(objective, n_trials=30)
best_params = study.best_params
print(f"✅ Best base params: {best_params}")


# PySR injection (unchanged)
from pysr import PySRRegressor
pysr = PySRRegressor(niterations=80, maxsize=12, random_state=42)
pysr.fit(synth[feature_cols], synth_y)
for df in [synth, real1, real2]:
    df['pysr_symbolic'] = pysr.predict(df[feature_cols])
feature_cols.append('pysr_symbolic')


# Expanded stacking function
def run_stacked_cv(df, y, name):
    X = df[feature_cols].copy()
    kf = KFold(n_splits=5, shuffle=True, random_state=42)
    r2_list, mse_list = [], []
    for tr_idx, val_idx in kf.split(X):
        X_tr, X_val = X.iloc[tr_idx], X.iloc[val_idx]
        y_tr, y_val = y.iloc[tr_idx], y.iloc[val_idx]
        # Base learners
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
        
        # Stack predictions
        stack_tr = np.column_stack((xgb_m.predict(X_tr), lgb_m.predict(X_tr), cat_m.predict(X_tr),
                                    hist_m.predict(X_tr), svr_m.predict(X_tr), pysr.predict(X_tr)))
        stack_val = np.column_stack((xgb_m.predict(X_val), lgb_m.predict(X_val), cat_m.predict(X_val),
                                     hist_m.predict(X_val), svr_m.predict(X_val), pysr.predict(X_val)))
        
        # Meta-learner
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
r2_synth, _ = run_stacked_cv(synth, synth_y, "Synthetic")
r2_real1, _ = run_stacked_cv(real1, real1_y, "Real1 JApJ")
r2_real2, _ = run_stacked_cv(real2, real2_y, "Real2 DESI/SDSS")


print("\n🎉 Step 19 Complete — Expanded Stacking with CatBoost + HistGB")
print("Reply with **analyze step 19** for full interpretation, tables, and next steps.")
