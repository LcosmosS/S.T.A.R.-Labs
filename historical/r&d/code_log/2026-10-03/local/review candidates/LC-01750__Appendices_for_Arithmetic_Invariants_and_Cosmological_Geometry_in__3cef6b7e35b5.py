    pysr_pred_test = pysr_model.predict(X_test_scaled).reshape(-1, 1)

    xgb_pred_train = xgb_model.predict(X_train_scaled).reshape(-1, 1)

    xgb_pred_test = xgb_model.predict(X_test_scaled).reshape(-1, 1)

    stack_train = np.hstack((X_train_scaled, pysr_pred_train, xgb_pred_train))

    stack_test = np.hstack((X_test_scaled, pysr_pred_test, xgb_pred_test))

    meta_model = XGBRegressor(n_estimators=100, learning_rate=0.05, max_depth=4,
random_state=42)

    meta_model.fit(stack_train, y_train)

    y_pred_stack = meta_model.predict(stack_test)



    r2_pysr = r2_score(y_test, pysr_pred_test)

    mae_pysr = mean_absolute_error(y_test, pysr_pred_test)

    r2_xgb = r2_score(y_test, xgb_pred_test)

    mae_xgb = mean_absolute_error(y_test, xgb_pred_test)

    r2_stack = r2_score(y_test, y_pred_stack)

    mae_stack = mean_absolute_error(y_test, y_pred_stack)



    print(f"{regime} PySR R²: {r2_pysr:.4f}, MAE: {mae_pysr:.4f}")

    print(f"{regime} XGBoost R²: {r2_xgb:.4f}, MAE: {mae_xgb:.4f}")

    print(f"{regime} Stacked R²: {r2_stack:.4f}, MAE: {mae_stack:.4f}")
