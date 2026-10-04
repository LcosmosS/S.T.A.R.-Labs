        if XGBRegressor:
            regressors.append(('XGBoost', XGBRegressor(random_state=42)))
        if LGBMRegressor:
            regressors.append(('LightGBM', LGBMRegressor(random_state=42)))
        if CatBoostRegressor and catboost_params_reg:
            regressors.append(('CatBoost', CatBoostRegressor(**catboost_params_reg,
verbose=0)))

        stacking_reg = StackingRegressor(estimators=regressors,
final_estimator=HistGradientBoostingRegressor(random_state=42))
        pipeline = Pipeline([
            ('scaler', StandardScaler(with_mean=False)),
            ('regressor', stacking_reg)
        ])
        pipeline.fit(X_tf, y_tf)
        tf_r2 = cross_val_score(pipeline, X_tf, y_tf, cv=5, scoring='r2').mean()
        print("Tully-Fisher R²:", tf_r2)

        tf_perm_importance = permutation_importance(pipeline.named_steps['regressor'],
X_tf, y_tf, n_repeats=10, random_state=42)
        tf_feature_importance = pd.Series(tf_perm_importance.importances_mean,
index=X_tf.columns).sort_values(ascending=False)
        print("\nTully-Fisher Feature Importance:\n", tf_feature_importance)

tf_feature_importance.to_csv(f'{OUTPUT_PLOT_PREFIX}_tully_fisher_feature_importance.cs
