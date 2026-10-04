# ────── DYNAMIC FEATURES ──────
def get_features(df):
    cols = ['scaled_a', 'scaled_b', 'flux_gr', 'pm_mag_proxy']
    for c in ['synth_betti_1', 'real1_betti_1', 'real2_betti_1']:
        if c in df.columns:
            cols.append(c)
    return [c for c in cols if c in df.columns]
# ────── STACKED MODEL (handles Series target for real data) ──────
def run_stacked_model(df, y, name):
    X = df[get_features(df)]
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=float(0.2), random_state=int(42)
    )
    from pysr import PySRRegressor
    pysr = PySRRegressor(niterations=int(100), maxsize=int(15), random_state=int(42))
    pysr.fit(X_train, y_train)
    xgb = XGBRegressor(n_estimators=int(200), learning_rate=float(0.03), max_depth=int(6), random_state=int(42))
    xgb.fit(X_train, y_train)
    train_stack = np.hstack((X_train, pysr.predict(X_train).reshape(-1,1), xgb.predict(X_train).reshape(-1,1)))
    test_stack = np.hstack((X_test, pysr.predict(X_test).reshape(-1,1), xgb.predict(X_test).reshape(-1,1)))
    meta = XGBRegressor(n_estimators=int(100), learning_rate=float(0.05), max_depth=int(4), random_state=int(42))
    meta.fit(train_stack, y_train)
    y_pred = meta.predict(test_stack)
    r2 = r2_score(y_test, y_pred)
    print(f" {name} Stacked R² = {r2:.4f}")
    return r2
print("\nTraining stacked models...")
r2_synth = run_stacked_model(synth, synth['exact_rank'], "Synthetic")
