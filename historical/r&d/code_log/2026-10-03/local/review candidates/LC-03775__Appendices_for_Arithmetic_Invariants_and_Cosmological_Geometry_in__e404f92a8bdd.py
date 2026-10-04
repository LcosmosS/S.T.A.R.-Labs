        df_list.append(chunk)

    df = pd.concat(df_list, ignore_index=True)

    # Compute cohomology
    df, betti_1 = compute_cohomology(df, entropy_col='entropy')

    # Compute entropy gradient
    df, entropy_gradient = compute_entropy_gradient(df)

    # Compute KDE features
    df, log_dens = compute_kde_features(df, 'selmer_rank', 'var_ap')

    # Check class distribution
    log_function("check_class_distribution")
    print("Generator Type Distribution:\n", df['generator_type'].value_counts())

    # NaN diagnostics
    log_function("nan_diagnostics")
    feature_cols = ['logmass', 'metallicity', 'petrorad_r', 'reg_cosmo', 't_cosmo',
'log_delta', 'log_omega',
