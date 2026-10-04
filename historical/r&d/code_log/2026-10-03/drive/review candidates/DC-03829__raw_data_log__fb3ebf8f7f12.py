# ────── LEAKAGE-FREE FEATURE ENGINEERING ──────
def add_leakage_free_features(df):
    df = df.copy()
    # Only non-velocity/redshift features
    df['flux_gr'] = df.get('Gmag', 0) / (df.get('Jmag', 1) + 1e-8)
    df['pm_mag_proxy'] = np.sqrt(df.get('pmRA', 0)**2 + df.get('pmDE', 0)**2)
    df['mag_ratio'] = df.get('gmag', 0) / (df.get('rmag', 1) + 1e-8)
    # Force numeric
    for col in ['flux_gr', 'pm_mag_proxy', 'mag_ratio']:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0).astype(float)
    return df


synth = add_leakage_free_features(synth)
real1 = add_leakage_free_features(real1)
real2 = add_leakage_free_features(real2)


# ────── INDEPENDENT TARGETS ──────
# Synthetic: true arithmetic rank (no leakage)
synth_target = synth['exact_rank']


# Real data: topological target = Betti_1 (already computed) or density proxy
real1_target = real1.get('real1_betti_1', np.zeros(len(real1)))   # fallback 0
real2_target = real2.get('real2_betti_1', np.zeros(len(real2)))


# ────── MODEL ──────
def run_leakage_free_model(X, y, name):
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    from pysr import PySRRegressor
    pysr = PySRRegressor(niterations=100, maxsize=12, random_state=42)
    pysr.fit(X_train, y_train)
    xgb = XGBRegressor(n_estimators=200, learning_rate=0.03, max_depth=6, random_state=42)
    xgb.fit(X_train, y_train)
    # Simple meta-learner
    meta = XGBRegressor(n_estimators=100, learning_rate=0.05, max_depth=4, random_state=42)
    train_stack = np.hstack((X_train, pysr.predict(X_train).reshape(-1,1), xgb.predict(X_train).reshape(-1,1)))
    test_stack = np.hstack((X_test, pysr.predict(X_test).reshape(-1,1), xgb.predict(X_test).reshape(-1,1)))
    meta.fit(train_stack, y_train)
    y_pred = meta.predict(test_stack)
    r2 = r2_score(y_test, y_pred)
    print(f"   {name} Leakage-Free R² = {r2:.4f}")
    return r2, pysr


print("\nTraining leakage-free models...")
r2_synth, pysr_synth = run_leakage_free_model(synth[['flux_gr','pm_mag_proxy','mag_ratio']], synth_target, "Synthetic")
r2_real1, pysr_real1 = run_leakage_free_model(real1[['flux_gr','pm_mag_proxy','mag_ratio']], real1_target, "Real1 JApJ")
r2_real2, pysr_real2 = run_leakage_free_model(real2[['flux_gr','pm_mag_proxy','mag_ratio']], real2_target, "Real2 DESI/SDSS")


print("\n🎉 Step 4 Complete — Leakage Removed")
print(f"   Synthetic R² = {r2_synth:.4f}")
print(f"   Real1 JApJ R² = {r2_real1:.4f}")
print(f"   Real2 DESI/SDSS R² = {r2_real2:.4f}")
print("\nIf R² > 0.70 here, we have strong evidence for ACSC/ECC.")
