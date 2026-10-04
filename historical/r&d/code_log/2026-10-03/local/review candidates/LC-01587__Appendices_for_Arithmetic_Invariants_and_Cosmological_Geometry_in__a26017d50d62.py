    print("  - Training predictive model on 75% of data...")
    pipeline.fit(X_train, y_train)

    print("  - Evaluating model on 25% unseen test data...")
    y_pred = pipeline.predict(X_test)

    r2 = r2_score(y_test, y_pred)
    print(f"  - Predictive Model R² Score on Test Set: {r2:.4f}")

    print("  - Analyzing model's ability to 'zero in' on the scaling factor K...")
    test_results = pd.DataFrame({
        'K_actual': y_test / X_test['discriminant'],
        'K_predicted': y_pred / X_test['discriminant']
    }).dropna()

    # Clip both for a fair comparison on the plot
    k_low_act, k_high_act = test_results['K_actual'].quantile(0.01),
