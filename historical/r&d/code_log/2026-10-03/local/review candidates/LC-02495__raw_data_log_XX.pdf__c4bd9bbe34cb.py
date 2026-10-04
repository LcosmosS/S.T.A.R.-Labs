    clf.fit(X_train, y_train_type)
    type_pred = (clf.predict(X_test) > 0.5).astype(int)
    acc = np.mean(type_pred == y_test_type)
    print(f"Dichotomy Accuracy: {acc:.3f}")

    # ——— REGRESSOR: Predict num_x, num_y (Recursive only) ———
    rec_idx = df["gen_type"] == "Recursive"
    X_rec = df[rec_idx][["r", "rho_star", "rank"]].values
    y_num_x = df[rec_idx]["num_x"].values
    y_num_y = df[rec_idx]["num_y"].values

    if len(X_rec) > 3:
        Xr_train, Xr_test, yx_train, yx_test, yy_train, yy_test = train_test_split(
            X_rec, y_num_x, y_num_y, test_size=0.3, random_state=42
        )

        # Gradient Boosters
        models = {
            "XGB": XGBRegressor(n_estimators=200),
            "LGBM": LGBMRegressor(n_estimators=200),
            "CatBoost": CatBoostRegressor(verbose=0, iterations=200)
        }

        best_r2 = -1
        best_model = None
        for name, model in models.items():
            model.fit(Xr_train, np.column_stack([yx_train, yy_train]))
            pred = model.predict(Xr_test)
            r2 = r2_score(np.column_stack([yx_test, yy_test]), pred)
            print(f"{name} R²: {r2:.3f}")
            if r2 > best_r2:
                best_r2 = r2
                best_model = model

        # ——— SYMBOLIC REGRESSION: Discover Sequence ———
        est = SymbolicRegressor(
            population_size=5000, generations=20,
            function_set=('add', 'sub', 'mul', 'div', 'log', 'sqrt'),
            metric='mse', parsimony_coefficient=0.01
        )
        est.fit(Xr_train, yx_train)
        print(f"Symbolic num_x: {est._program}")

        est.fit(Xr_train, yy_train)
        print(f"Symbolic num_y: {est._program}")

    return clf, best_model, acc

# ————————————————————————