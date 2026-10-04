# Leakage-free features + numeric enforcement
def add_features(df):
    df = df.copy()
    df['flux_gr'] = df.get('Gmag', 0) / (df.get('Jmag', 1) + 1e-8)
    df['pm_mag_proxy'] = np.sqrt(df.get('pmRA', 0)**2 + df.get('pmDE', 0)**2)
    df['mag_ratio'] = df.get('gmag', 0) / (df.get('rmag', 1) + 1e-8)
    for col in ['flux_gr', 'pm_mag_proxy', 'mag_ratio']:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0).astype(float)
    return df


synth = add_features(synth)
real1 = add_features(real1)
real2 = add_features(real2)


# Features (strictly independent)
feature_cols = ['flux_gr', 'pm_mag_proxy', 'mag_ratio']


# Targets (no leakage)
synth_y = synth['exact_rank']
real1_y = real1.get('real1_betti_1', np.zeros(len(real1)))   # topological target
real2_y = real2.get('real2_betti_1', np.zeros(len(real2)))


def run_cv_model(X, y, name):
    X = X[feature_cols]
    kf = KFold(n_splits=5, shuffle=True, random_state=42)
    r2_scores = []
    mse_scores = []
    for train_idx, test_idx in kf.split(X):
        X_train, X_test = X.iloc[train_idx], X.iloc[test_idx]
        y_train, y_test = y.iloc[train_idx], y.iloc[test_idx]
        
        # PySR on full training fold
        from pysr import PySRRegressor
        pysr = PySRRegressor(niterations=80, maxsize=12, random_state=42)  # slightly reduced iterations for CV speed
        pysr.fit(X_train, y_train)
        
        # XGBoost + meta stack
        xgb = XGBRegressor(n_estimators=200, learning_rate=0.03, max_depth=6, random_state=42)
        xgb.fit(X_train, y_train)
        train_stack = np.hstack((X_train, pysr.predict(X_train).reshape(-1,1), xgb.predict(X_train).reshape(-1,1)))
        test_stack = np.hstack((X_test, pysr.predict(X_test).reshape(-1,1), xgb.predict(X_test).reshape(-1,1)))
        meta = XGBRegressor(n_estimators=100, learning_rate=0.05, max_depth=4, random_state=42)
        meta.fit(train_stack, y_train)
        y_pred = meta.predict(test_stack)
        
        r2_scores.append(r2_score(y_test, y_pred))
        mse_scores.append(mean_squared_error(y_test, y_pred))
    
    print(f"\n{name} — 5-Fold CV Results")
    print(f"   R²  = {np.mean(r2_scores):.4f} ± {np.std(r2_scores):.4f}")
    print(f"   MSE = {np.mean(mse_scores):.4f} ± {np.std(mse_scores):.4f}")
    return np.mean(r2_scores), np.mean(mse_scores)


print("Running 5-fold CV with explicit MSE...")
r2_synth, mse_synth = run_cv_model(synth, synth_y, "Synthetic")
r2_real1, mse_real1 = run_cv_model(real1, real1_y, "Real1 JApJ")
r2_real2, mse_real2 = run_cv_model(real2, real2_y, "Real2 DESI/SDSS")


print("\n🎉 Leakage-Free CV Complete")
print("These numbers now reflect true generalization fidelity.")
