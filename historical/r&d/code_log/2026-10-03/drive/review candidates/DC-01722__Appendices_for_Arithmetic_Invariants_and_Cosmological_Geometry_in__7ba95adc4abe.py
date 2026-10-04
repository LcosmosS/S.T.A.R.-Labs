    if XGBClassifier:
        classifiers.append(('XGBoost', XGBClassifier(random_state=42)))
    if LGBMClassifier:
        classifiers.append(('LightGBM', LGBMClassifier(random_state=42)))
    if CatBoostClassifier and catboost_params_clf:
        classifiers.append(('CatBoost', CatBoostClassifier(**catboost_params_clf, verbose=0)))


    stacking_clf = StackingClassifier(estimators=classifiers, final_estimator=HistGradientBoostingClassifier(random_state=42))
    stacking_clf.fit(X, y)
    gen_accuracy = cross_val_score(stacking_clf, X, y, cv=5).mean()
    print("Stacking Classifier Accuracy:", gen_accuracy)
    print("Classification Report:\n", classification_report(y, stacking_clf.predict(X)))


    # Feature importance
    log_function("compute_generator_feature_importance")
    gen_perm_importance = permutation_importance(stacking_clf, X, y, n_repeats=10, random_state=42)
    gen_feature_importance = pd.Series(gen_perm_importance.importances_mean, index=X.columns).sort_values(ascending=False)
    print("\nGenerator Type Feature Importance:\n", gen_feature_importance)
    gen_feature_importance.to_csv(f'{OUTPUT_PLOT_PREFIX}_generator_feature_importance.csv')


    plt.figure(figsize=(10, 6))
    sns.barplot(x=gen_feature_importance.values, y=gen_feature_importance.index)
    plt.title('Generator Type Feature Importance')
    plt.savefig(f'{OUTPUT_PLOT_PREFIX}_generator_feature_importance.png')
    plt.close()


    # Symbolic regression for generator type
    log_function("symbolic_regression_generator")
    for method in ['pysr', 'gplearn']:
        sym_reg_gen = run_symbolic_regression(X, y.map({'Simple': 0, 'Recursive': 1, 'unknown': 2}), feature_cols, method)
        if sym_reg_gen:
            getattr(sym_reg_gen, 'equations_', pd.DataFrame()).to_csv(f'{OUTPUT_PLOT_PREFIX}_symbolic_regression_generator_{method}.csv')


    # Clustering
    log_function("perform_clustering")
    X_struct = df[df['generator_type'] == 'Recursive'][['logmass', 'metallicity', 'petrorad_r', 'log_delta', 'log_omega', 'entropy', 'kde_selmer_rank_var_ap']]
    cluster_labels = None
    if not X_struct.empty:
        X_struct = preprocess_clustering_features(X_struct, ['logmass', 'metallicity', 'petrorad_r', 'log_delta', 'log_omega', 'entropy', 'kde_selmer_rank_var_ap'])
        dbscan = DBSCAN(eps=0.5, min_samples=5, metric='nan_euclidean')
        cluster_labels = dbscan.fit_predict(X_struct)
        df.loc[df['generator_type'] == 'Recursive', 'structure_cluster'] = cluster_labels
        print("Structure Clusters:", df[df['generator_type'] == 'Recursive']['structure_cluster'].value_counts())
        kmeans = KMeans(n_clusters=5, random_state=42)
        kmeans_labels = kmeans.fit_predict(X_struct)
        df.loc[df['generator_type'] == 'Recursive', 'kmeans_cluster'] = kmeans_labels
        print("KMeans Clusters:", df[df['generator_type'] == 'Recursive']['kmeans_cluster'].value_counts())


    # Shape analysis
    analyze_noise_points(df, feature_cols)


    # Tully-Fisher test
    log_function("tully_fisher_test")
    X_tf = df[feature_cols]
    y_tf = df['petrorad_r']
    valid_idx = y_tf.notna()
    X_tf = X_tf[valid_idx]
    y_tf = y_tf[valid_idx]
    print(f"Tully-Fisher: Dropped {len(df) - len(X_tf)} rows due to NaN in petrorad_r")
    if not X_tf.empty:
        catboost_params_reg = optimize_catboost_regressor(X_tf, y_tf) if CatBoostRegressor and create_study else None
        regressors = [
            ('RandomForest', RandomForestRegressor(random_state=42)),
            ('HistGradientBoosting', HistGradientBoostingRegressor(random_state=42))
