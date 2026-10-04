    r2_stack = r2_score(y_test, y_pred_stack)

    mae_stack = mean_absolute_error(y_test, y_pred_stack)



    print(f"{regime} PySR R²: {r2_pysr:.4f}, MAE: {mae_pysr:.4f}")

    print(f"{regime} XGBoost R²: {r2_xgb:.4f}, MAE: {mae_xgb:.4f}")

    print(f"{regime} Stacked R²: {r2_stack:.4f}, MAE: {mae_stack:.4f}")



    return pysr_model, xgb_model, meta_model, X_test, y_pred_pysr, y_pred_xgb, y_pred_stack



# Run for regime

for regime, dfr in [('galactic', df_gal), ('cluster', df_clust)]:

    if len(dfr) < 2: continue

    Xr = dfr[X_clf_cols]

    yr = dfr['z']

    pysr_model, xgb_model, meta_model, X_test, y_pred_pysr, y_pred_xgb, y_pred_stack =
run_models(Xr, yr, regime.capitalize())



    X_test_df = pd.DataFrame(X_test, columns=X_clf_cols)

    X_test_df['predicted_type'] = gen_clf.predict(X_test)



    # PNG Scatter (PySR)
