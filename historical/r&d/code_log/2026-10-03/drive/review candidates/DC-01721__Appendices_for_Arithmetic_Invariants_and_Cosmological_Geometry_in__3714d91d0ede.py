        chunk['generator_coords'] = chunk['log_delta'].apply(lambda x: (x, x*2) if not pd.isna(x) else np.nan)
        chunk['generator_structure'] = chunk['generator_coords'].apply(analyze_generator_structure)


        df_list.append(chunk)


    df = pd.concat(df_list, ignore_index=True)


    # Check class distribution
    log_function("check_class_distribution")
    print("Generator Type Distribution:\n", df['generator_type'].value_counts())


    # NaN diagnostics
    log_function("nan_diagnostics")
    feature_cols = ['logmass', 'metallicity', 'petrorad_r', 'reg_cosmo', 't_cosmo', 'log_delta', 'log_omega',
                    'log_torsion', 'log_conductor', 'real_log_j', 'imag_log_j', 'tr_p1', 'var_ap', 'sato_tate',
                    'isogeny_count', 'log_min_isogeny', 'log_torsion_type', 'is_simple_generator', 'selmer_rank',
                    'torsion', 'j_invariant', 'discriminant', 'entropy', 'kde_selmer_rank_var_ap']
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
    catboost_params_clf = optimize_catboost_classifier(X, y) if CatBoostClassifier and create_study else None
    classifiers = [
        ('RandomForest', RandomForestClassifier(random_state=42)),
        ('GradientBoosting', GradientBoostingClassifier(random_state=42))
