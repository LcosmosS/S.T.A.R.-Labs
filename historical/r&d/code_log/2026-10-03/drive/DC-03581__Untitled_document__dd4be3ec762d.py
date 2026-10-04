        if XGBRegressor:
            regressors.append(('XGBoost', XGBRegressor(random_state=42)))
        if LGBMRegressor:
            regressors.append(('LightGBM', LGBMRegressor(random_state=42)))
        if CatBoostRegressor and catboost_params_reg:
            regressors.append(('CatBoost', CatBoostRegressor(**catboost_params_reg, verbose=0)))


        stacking_reg = StackingRegressor(estimators=regressors, final_estimator=HistGradientBoostingRegressor(random_state=42))
        pipeline = Pipeline([
            ('scaler', StandardScaler(with_mean=False)),
            ('regressor', stacking_reg)
        ])
        pipeline.fit(X_tf, y_tf)
        tf_r2 = cross_val_score(pipeline, X_tf, y_tf, cv=5, scoring='r2').mean()
        print("Tully-Fisher R²:", tf_r2)


        tf_perm_importance = permutation_importance(pipeline.named_steps['regressor'], X_tf, y_tf, n_repeats=10, random_state=42)
        tf_feature_importance = pd.Series(tf_perm_importance.importances_mean, index=X_tf.columns).sort_values(ascending=False)
        print("\nTully-Fisher Feature Importance:\n", tf_feature_importance)
        tf_feature_importance.to_csv(f'{OUTPUT_PLOT_PREFIX}_tully_fisher_feature_importance.csv')


        plt.figure(figsize=(10, 6))
        sns.barplot(x=tf_feature_importance.values, y=tf_feature_importance.index)
        plt.title('Tully-Fisher Feature Importance')
        plt.savefig(f'{OUTPUT_PLOT_PREFIX}_tully_fisher_feature_importance.png')
        plt.close()


        for method in ['pysr', 'gplearn']:
            sym_reg_tf = run_symbolic_regression(X_tf, y_tf, feature_cols, method)
            if sym_reg_tf:
                getattr(sym_reg_tf, 'equations_', pd.DataFrame()).to_csv(f'{OUTPUT_PLOT_PREFIX}_symbolic_regression_tully_fisher_{method}.csv')


    # PCA and t-SNE
    log_function("dimensionality_reduction")
    X_valid = df[feature_cols].dropna()
    if not X_valid.empty:
        pca = PCA(n_components=2)
        X_pca = pca.fit_transform(X_valid)
        df_pca = pd.DataFrame(X_pca, columns=['PC1', 'PC2'], index=X_valid.index)
        df_pca['generator_type'] = df.loc[X_valid.index, 'generator_type']
        plt.figure(figsize=(10, 6))
        sns.scatterplot(data=df_pca, x='PC1', y='PC2', hue='generator_type')
        plt.title('PCA of Galaxy Features with Entropy')
        plt.savefig(f'{OUTPUT_PLOT_PREFIX}_pca_scatter_entropy.png')
        plt.close()


    # Interactive visualization
    interactive_visualization(df, feature_cols)


    # Save results
    log_function("save_results")
    df.to_csv(f'{OUTPUT_PLOT_PREFIX}_processed.csv', index=False)


if __name__ == "__main__":
    main()
