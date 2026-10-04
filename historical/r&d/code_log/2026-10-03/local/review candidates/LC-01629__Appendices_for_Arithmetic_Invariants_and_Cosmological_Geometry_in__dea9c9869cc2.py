    pipeline = Pipeline([('scaler', StandardScaler()), ('model',
lgb.LGBMRegressor(random_state=42))])
    print("  - Training predictive model on 75% of data in Log-Stable space...")
    pipeline.fit(X_train, y_train)

    print("  - Evaluating model on 25% unseen test data...")
    y_pred_log = pipeline.predict(X_test)
    r2 = r2_score(y_test, y_pred_log)
    print(f"  - Predictive Model R² Score (in Log-Space) on Test Set: {r2:.4f}")

    print("  - Analyzing model's ability to 'zero in' on the scaling factor K...")
    # Get original, non-log values from the test set's index
    original_test_data = df.loc[X_test.index]

    # Convert predicted log energy back to real energy
    # We must re-introduce the negative sign of the original Virial energy
    predicted_virial_energy = -(10**y_pred_log)

    test_results = pd.DataFrame({
        'K_actual': original_test_data['virial_energy_j'] /
