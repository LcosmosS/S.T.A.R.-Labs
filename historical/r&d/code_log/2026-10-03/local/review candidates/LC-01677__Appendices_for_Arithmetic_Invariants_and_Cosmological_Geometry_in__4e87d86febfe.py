        df_list.append(chunk)

    df = pd.concat(df_list, ignore_index=True)

    # Check class distribution
    log_function("check_class_distribution")
    print("Generator Type Distribution:\n", df['generator_type'].value_counts())

    # NaN diagnostics
    log_function("nan_diagnostics")
    feature_cols = ['logmass', 'metallicity', 'petrorad_r', 'reg_cosmo', 't_cosmo',
'log_delta', 'log_omega',
                    'log_torsion', 'log_conductor', 'real_log_j', 'imag_log_j',
'tr_p1', 'var_ap', 'sato_tate',
                    'isogeny_count', 'log_min_isogeny', 'log_torsion_type',
'is_simple_generator', 'selmer_rank',
                    'torsion', 'j_invariant', 'discriminant', 'entropy',
