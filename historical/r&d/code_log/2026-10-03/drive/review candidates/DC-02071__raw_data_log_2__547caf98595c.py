# ====================== THESIS METRICS ======================
def add_thesis_features(df):
    df = df.copy()
    df['flux_gr'] = df.get('Gmag', 0) / (df.get('Jmag', 1) + 1e-8)
    df['pm_mag_proxy'] = np.sqrt(df.get('pmRA', 0)**2 + df.get('pmDE', 0)**2)
    df['mag_ratio'] = df.get('gmag', 0) / (df.get('rmag', 1) + 1e-8)
    if 'zphot' in df.columns:
        df['T_cosmo'] = 1.0 / (1.0 + df['zphot'])
    elif 'Vcmb' in df.columns:
        df['T_cosmo'] = 1.0 / (1.0 + df['Vcmb'] / 3e5)
    else:
        df['T_cosmo'] = 1.0
    if 'Vcmb' in df.columns:
        df['Tully_Fisher'] = df.get('gmag', 0) + 5 * np.log10(df['Vcmb'] / 100.0)
    else:
        df['Tully_Fisher'] = df.get('gmag', 0)
    for col in ['flux_gr', 'pm_mag_proxy', 'mag_ratio', 'T_cosmo', 'Tully_Fisher']:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0).astype(float)
    return df


synth = add_thesis_features(synth)
real1 = add_thesis_features(real1)
real2 = add_thesis_features(real2)


# ====================== PHYSICAL TOPOLOGY (FULL FUNCTION) ======================
def add_physical_local_topology(df, name, ra_col, de_col, z_col, k=25):
    if z_col in df.columns:
        if z_col == 'Vcmb':
            z = df[z_col].values / 3e5
        else:
            z = df[z_col].values
    else:
        z = np.zeros(len(df))
    comoving_dist = z * 4285.7
    ra_rad = np.deg2rad(df[ra_col].values)
    de_rad = np.deg2rad(df[de_col].values)
    coords = np.column_stack((
        comoving_dist * np.cos(de_rad) * np.cos(ra_rad),
        comoving_dist * np.cos(de_rad) * np.sin(ra_rad),
        comoving_dist * np.sin(de_rad)
    ))
    nn = NearestNeighbors(n_neighbors=k).fit(coords)
    distances, _ = nn.kneighbors(coords)
    adaptive_scale = np.percentile(distances[:, -1], 50)
    print(f"   {name} adaptive scale = {adaptive_scale:.2f} Mpc (k={k})")
    df[name + '_local_density'] = distances.mean(axis=1)
    df['Anthropic'] = np.abs(df[name + '_local_density'] - np.median(df[name + '_local_density']))
    local_betti = np.zeros((len(coords), 3), dtype=int)
    for i in range(len(coords)):
        neigh_idx = nn.kneighbors(coords[i].reshape(1, -1), return_distance=False)[0]
        neigh_points = coords[neigh_idx]
        rips = gudhi.RipsComplex(points=neigh_points, max_edge_length=adaptive_scale)
        st = rips.create_simplex_tree(max_dimension=2)
        st.compute_persistence()
        betti = st.betti_numbers()
        for j in range(3):
            local_betti[i, j] = betti[j] if len(betti) > j else 0
    for i in range(3):
        df[name + f'_local_betti_{i}'] = local_betti[:, i]
    print(f"   {name} per-galaxy local Betti_0/1/2 computed")
    return df


print("\nComputing topology...")
real1 = add_physical_local_topology(real1, "real1", "RAJ2000", "DEJ2000", "Vcmb")
real2 = add_physical_local_topology(real2, "real2", "RAdeg", "DEdeg", "zphot")
synth = add_physical_local_topology(synth, "synth", "synthetic_RA", "synthetic_DE", "synthetic_z")


feature_cols = ['flux_gr', 'pm_mag_proxy', 'mag_ratio', 'T_cosmo', 'Tully_Fisher', 'Anthropic',
                'real1_local_betti_2', 'real2_local_betti_2', 'synth_local_betti_2']


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
    X = synth[feature_cols].copy()
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
pysr.fit(synth[feature_cols], synth_y)
for df in [synth, real1, real2]:
    df['pysr_symbolic'] = pysr.predict(df[feature_cols])
feature_cols.append('pysr_symbolic')


# ====================== EXPANDED STACKING ======================
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
r2_synth, _ = run_stacked_cv(synth, synth_y, "Synthetic")
r2_real1, _ = run_stacked_cv(real1, real1_y, "Real1 JApJ")
r2_real2, _ = run_stacked_cv(real2, real2_y, "Real2 DESI/SDSS")


print("\n🎉 Step 19 Complete — Expanded Stacking")
print("Reply with **analyze step 19** for full interpretation, tables, and conclusions.")
