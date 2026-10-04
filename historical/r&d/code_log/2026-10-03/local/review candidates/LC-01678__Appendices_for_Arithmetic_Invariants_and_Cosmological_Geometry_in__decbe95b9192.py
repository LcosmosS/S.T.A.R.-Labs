    nan_counts = df[feature_cols[:-1]].isna().sum()
    print("NaN Counts in Features:\n", nan_counts)
    nan_counts.to_csv(f'{OUTPUT_PLOT_PREFIX}_nan_counts.csv')

    # Compute KDE features
    df, log_dens = compute_kde_features(df, 'selmer_rank', 'var_ap')

    # Impute derived features
    df = impute_derived_features(df, feature_cols)

    # Machine learning models for generator type
    X = df[feature_cols]
    y = df['generator_type']

    # Optimize CatBoost
    catboost_params_clf = optimize_catboost_classifier(X, y) if CatBoostClassifier and
create_study else None
    classifiers = [
        ('RandomForest', RandomForestClassifier(random_state=42)),
        ('GradientBoosting', GradientBoostingClassifier(random_state=42))
