# Leakage-free photometric features only
def add_photometric_features(df):
    df = df.copy()
    df['flux_gr'] = df.get('Gmag', 0) / (df.get('Jmag', 1) + 1e-8)
    df['pm_mag_proxy'] = np.sqrt(df.get('pmRA', 0)**2 + df.get('pmDE', 0)**2)
    df['mag_ratio'] = df.get('gmag', 0) / (df.get('rmag', 1) + 1e-8)
    for col in ['flux_gr', 'pm_mag_proxy', 'mag_ratio']:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0).astype(float)
    return df


synth = add_photometric_features(synth)
real1 = add_photometric_features(real1)
real2 = add_photometric_features(real2)


feature_cols = ['flux_gr', 'pm_mag_proxy', 'mag_ratio']


# ────── COMPUTE REAL BETTI_1 + DENSITY PROXY ──────
def compute_topological_features(df, name, ra_col, de_col, z_col, n_points=10000):
    # Subsample for memory safety
    sample_df = df[[ra_col, de_col, z_col]].dropna()
    sample = sample_df.sample(n=min(int(n_points), len(sample_df)), random_state=int(42)).values
    if len(sample) < 100:
        df[name + '_betti_1'] = 0
        df[name + '_density_gradient'] = 0
        return df
    # Betti_1 (Entropy Cohomology)
    rips = gudhi.RipsComplex(points=sample, max_edge_length=1.0)
    st = rips.create_simplex_tree(max_dimension=2)
    st.compute_persistence()
    betti = st.betti_numbers()
    df[name + '_betti_1'] = betti[1] if len(betti) > 1 else 0
    print(f"   {name} Betti_1 computed")
    # Local density gradient proxy
    nn = NearestNeighbors(n_neighbors=10).fit(sample)
    distances, _ = nn.kneighbors(sample)
    df[name + '_density_gradient'] = distances.mean(axis=1).mean()  # scalar proxy per dataset
    print(f"   {name} density gradient computed")
    return df


print("\nComputing real topological features...")
real1 = compute_topological_features(real1, "real1", "RAJ2000", "DEJ2000", "Vcmb")
real2 = compute_topological_features(real2, "real2", "RAdeg", "DEdeg", "zphot")


# Targets (true topological)
synth_y = synth['exact_rank']
real1_y = real1['real1_betti_1']
real2_y = real2['real2_betti_1']


# 5-fold CV
def run_cv(X, y, name):
    X = X[feature_cols].copy()
    kf = KFold(n_splits=5, shuffle=True, random_state=42)
    r2_scores, mse_scores = [], []
    for train_idx, test_idx in kf.split(X):
        X_train, X_test = X.iloc[train_idx], X.iloc[test_idx]
        y_train, y_test = y.iloc[train_idx], y.iloc[test_idx]
        xgb = XGBRegressor(n_estimators=200, learning_rate=0.03, max_depth=6, random_state=42)
        xgb.fit(X_train, y_train)
        y_pred = xgb.predict(X_test)
        r2_scores.append(r2_score(y_test, y_pred))
        mse_scores.append(mean_squared_error(y_test, y_pred))
    print(f"\n{name} — 5-Fold CV (Topological Target)")
    print(f"   R²  = {np.mean(r2_scores):.4f} ± {np.std(r2_scores):.4f}")
    print(f"   MSE = {np.mean(mse_scores):.4f} ± {np.std(mse_scores):.4f}")
    return np.mean(r2_scores), np.mean(mse_scores)


print("\nRunning 5-fold CV...")
r2_synth, mse_synth = run_cv(synth, synth_y, "Synthetic")
r2_real1, mse_real1 = run_cv(real1, real1_y, "Real1 JApJ")
r2_real2, mse_real2 = run_cv(real2, real2_y, "Real2 DESI/SDSS")


# PySR + outputs on synthetic
print("\nRunning PySR on synthetic...")
from pysr import PySRRegressor
pysr = PySRRegressor(niterations=80, maxsize=12, random_state=42)
pysr.fit(synth[feature_cols], synth_y)
pysr.get_hall_of_fame().to_csv("hall_of_fame_final.csv", index=False)
print("✅ hall_of_fame_final.csv saved")


xgb = XGBRegressor(n_estimators=200, learning_rate=0.03, max_depth=6, random_state=42)
xgb.fit(synth[feature_cols], synth_y)
imp = pd.DataFrame({'feature': feature_cols, 'importance': xgb.feature_importances_}).sort_values('importance', ascending=False)
imp.to_csv("feature_importance.csv", index=False)
print("✅ feature_importance.csv saved")


pred_df = pd.DataFrame({
    'true_target': synth['exact_rank'],
    'flux_gr': synth['flux_gr'],
    'pm_mag_proxy': synth['pm_mag_proxy'],
    'mag_ratio': synth['mag_ratio']
})
pred_df.to_csv("predictions_final.csv", index=False)
print("✅ predictions_final.csv saved")


print("\n🎉 Step 6 Complete — Real Betti_1 + Density Proxies Added")
print("Reply with **analyze step 6** for full interpretation of the new scores.")
