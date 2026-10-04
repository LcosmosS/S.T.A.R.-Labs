    # Evaluate
    print("\n--- Global Sweep Results (Combined real1 + real2) ---")
    y_test = test_df['persistence_entropy']
    preds = sweep_stacker.predict(test_df[features])

    for s in [0, 1, 2]:
        mask = (test_df['entropy_strata'] == s)
        if mask.sum() > 0:
            s_true, s_pred = y_test[mask], preds[mask]
            if np.var(s_true) < 1e-8:
                print(f" Stratum {s} (Voids): MAE = {mean_absolute_error(s_true, s_pred):.6f}
