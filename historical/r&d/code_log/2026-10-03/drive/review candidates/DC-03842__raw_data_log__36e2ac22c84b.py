# Leakage-free features only
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


# Leakage-free feature selector
def get_features(df):
    cols = ['flux_gr', 'pm_mag_proxy', 'mag_ratio']   # only photometric features
    return [c for c in cols if c in df.columns]


# Your working stacked model
def run_stacked_model(df, y, name):
    X = df[get_features(df)]
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=float(0.2), random_state=int(42)
    )
    from pysr import PySRRegressor
    pysr = PySRRegressor(niterations=int(80), maxsize=int(12), random_state=int(42))
    pysr.fit(X_train, y_train)
    xgb = XGBRegressor(n_estimators=int(200), learning_rate=float(0.03), max_depth=int(6), random_state=int(42))
    xgb.fit(X_train, y_train)
    train_stack = np.hstack((X_train, pysr.predict(X_train).reshape(-1,1), xgb.predict(X_train).reshape(-1,1)))
    test_stack = np.hstack((X_test, pysr.predict(X_test).reshape(-1,1), xgb.predict(X_test).reshape(-1,1)))
    meta = XGBRegressor(n_estimators=int(100), learning_rate=float(0.05), max_depth=int(4), random_state=int(42))
    meta.fit(train_stack, y_train)
    y_pred = meta.predict(test_stack)
    r2 = r2_score(y_test, y_pred)
    print(f"   {name} Stacked R² = {r2:.4f}")
    return r2, pysr


print("\nTraining leakage-free stacked model on synthetic...")
r2_synth, pysr_model = run_stacked_model(synth, synth['exact_rank'], "Synthetic")


# Save outputs
pysr_model.get_hall_of_fame().to_csv("hall_of_fame_final.csv", index=False)
print("✅ hall_of_fame_final.csv saved")


xgb = XGBRegressor(n_estimators=200, learning_rate=0.03, max_depth=6, random_state=42)
xgb.fit(synth[get_features(synth)], synth['exact_rank'])
imp = pd.DataFrame({'feature': get_features(synth), 'importance': xgb.feature_importances_})
imp = imp.sort_values('importance', ascending=False)
imp.to_csv("feature_importance.csv", index=False)
print("✅ feature_importance.csv saved")


pred_df = pd.DataFrame({
    'true_rank': synth['exact_rank'],
    'flux_gr': synth['flux_gr'],
    'pm_mag_proxy': synth['pm_mag_proxy'],
    'mag_ratio': synth['mag_ratio']
})
pred_df.to_csv("predictions_final.csv", index=False)
print("✅ predictions_final.csv saved")


print("\n🎉 All outputs generated successfully!")
print("Reply with **analyze step 4** for full interpretation, tables, and thesis text.")
