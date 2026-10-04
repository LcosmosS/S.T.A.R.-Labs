    df['cosmo_rank'] = 0.5 * gz_df['Num_w_norm'] + 0.3 * gz_df['morph_norm'] + 0.2 * gz_df['redshift_norm']
    print("Computed cosmo_rank using ellipticity and redshift proxies.")
else:
    print("Warning: ellipticity or redshift missing. Setting cosmo_rank to 0.5.")
    df['cosmo_rank'] = 0.5


# Ensure cosmo_rank is numeric and imputed ============================================================================================================================
df['cosmo_rank'] = pd.to_numeric(df['cosmo_rank'], errors='coerce').replace([np.inf, -np.inf], np.nan).fillna(0.5)


# Step 2: L_cosmo(s) Construction =====================================================================================================================================
if 'logmass' in df.columns:
    df['logMass'] = df['logmass']
if 'petrorad_r' in df.columns:
    df['kronRad'] = df['petrorad_r']


alpha = -1.5
if 'logMass' in df.columns and 'kronRad' in df.columns:
    df['log_Mass_gas'] = df['logMass']
    M_star = df['log_Mass_gas'].median()
    df['a_n'] = (10 ** df['log_Mass_gas'])**(1 + alpha) * np.exp(-10 ** df['log_Mass_gas'] / (10 ** M_star))
    
# = Preprocess kronRad ------------------------------------------------------------------------------------------
    df['kronRad'] = df['kronRad'].replace([np.inf, -np.inf], np.nan).fillna(df['kronRad'].median(skipna=True))
    if df['kronRad'].isna().all():
        print("Warning: kronRad is all NaN after preprocessing. Setting L_cosmo_s_* to 0.")
        for s in [0.5, 1.0, 1.5, 2.0]:
            df[f'L_cosmo_s_{s:.1f}'] = 0
    else:


# ======= Try quantile binning first ------------------------------------------------------------------------------
        try:
            bins = pd.qcut(df['kronRad'], q=20, labels=False, duplicates='drop') + 1
            df['z_bin'] = bins
            n_bins = df['z_bin'].nunique()
            print(f"Number of unique bins (qcut): {n_bins}")
            print("Bin distribution for kronRad (qcut):")
            print(df['z_bin'].value_counts().sort_index())
        except Exception as e:
            print(f"Warning: pd.qcut failed due to {e}. Falling back to pd.cut.")


# ======== Fallback to equal-width binning ---------------------------------------------------------------------------
            try:
                bins = pd.cut(df['kronRad'], bins=20, labels=False, duplicates='drop') + 1
                df['z_bin'] = bins
                n_bins = df['z_bin'].nunique()
                print(f"Number of unique bins (cut): {n_bins}")
                print("Bin distribution for kronRad (cut):")
                print(df['z_bin'].value_counts().sort_index())
            except Exception as e:
                print(f"Warning: pd.cut also failed due to {e}. Using median-based fallback.")
                df['z_bin'] = (df['kronRad'] > df['kronRad'].median()).astype(int) + 1  # Binary split
                n_bins = df['z_bin'].nunique()
                print(f"Number of unique bins (fallback): {n_bins}")
                print("Bin distribution for kronRad (fallback):")
                print(df['z_bin'].value_counts().sort_index())


# ======== Ensure a minimum number of bins ---------------------------------------------------------------------------------
        if n_bins < 5:
