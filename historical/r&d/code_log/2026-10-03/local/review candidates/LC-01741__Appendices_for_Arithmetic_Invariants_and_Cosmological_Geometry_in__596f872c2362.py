        random_state=42,

        deterministic=True,

        parallelism='serial',

        constraints={'^': (-1, 1)}

    )

    pysr_model.fit(X_train_scaled, y_train)

    pysr_eq = pysr_model.sympy()

    y_pred_pysr = pysr_model.predict(X_test_scaled)

    r2_pysr = r2_score(y_test, y_pred_pysr)

    mae_pysr = mean_absolute_error(y_test, y_pred_pysr)



    # XGBoost Boosting

    xgb_model = XGBRegressor(n_estimators=100, learning_rate=0.05, max_depth=5,
random_state=42)

    xgb_model.fit(X_train_scaled, y_train)

    y_pred_xgb = xgb_model.predict(X_test_scaled)

    r2_xgb = r2_score(y_test, y_pred_xgb)

    mae_xgb = mean_absolute_error(y_test, y_pred_xgb)



    print(f"{regime.capitalize()} PySR Eq:", pysr_eq)

    print(f"{regime.capitalize()} PySR R²: {r2_pysr:.4f}, MAE: {mae_pysr:.4f}")