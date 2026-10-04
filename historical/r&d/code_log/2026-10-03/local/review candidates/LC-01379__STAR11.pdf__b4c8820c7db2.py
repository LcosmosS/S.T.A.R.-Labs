            df['z_bin'] = (df['kronRad'] > df['kronRad'].median()).astype(int) + 1  # Binary split
            n_bins = df['z_bin'].nunique()
            print(f"Adjusted number of unique bins: {n_bins}")
            print("Adjusted bin distribution for kronRad:")
            print(df['z_bin'].value_counts().sort_index())

# ======== Compute L_cosmo_s_* features ---------------------------------------------------------------------------------------
        s_vals = [0.5, 1.0, 1.5, 2.0]
        for s in s_vals:
            col_name = f'L_cosmo_s_{s:.1f}'
            df[col_name] = df.groupby('z_bin')['a_n'].transform('mean') / (df['z_bin'] ** s)

# ======== Replace any NaN or inf values in L_cosmo_s_* with 0 -----------------------------------------------------------------
            df[col_name] = df[col_name].replace([np.inf, -np.inf], np.nan).fillna(0)
            print(f"Created {col_name}")
else:
    print("Warning: logMass or kronRad missing. Setting L_cosmo_s_* to 0.")
    for s in [0.5, 1.0, 1.5, 2.0]:
        df[f'L_cosmo_s_{s:.1f}'] = 0

# Diagnostics for L_cosmo_s_* features
=========================================================================================
=======================================
print(f"cosmo_rank: mean={df['cosmo_rank'].mean():.4f}, std={df['cosmo_rank'].std():.4f}")
for s in [0.5, 1.0, 1.5, 2.0]:
    col = f'L_cosmo_s_{s:.1f}'
    print(f"{col}: mean={df[col].mean():.4f}, std={df[col].std():.4f}, NaN={df[col].isna().sum()},
Inf={np.isinf(df[col]).sum()}")

# Feature engineering with proper cosmic measurements
=========================================================================================
========================
df['log_Mass'] = df['log_Mass_gas']

# Check for missing columns and compute if necessary
=========================================================================================
=========================
required_cols = {
    'SpecObj': 'SpecObj',
    'OH_O3N2_cen': 'OH_O3N2_cen',
    'OH_T04_cen': 'OH_T04_cen',
    'Av_gas_Re': 'Av_gas_Re',
    'vel_disp_Ha_cen': 'vel_disp_Ha_cen',
    'Sigma_Mass_Re': 'Sigma_Mass_Re',
    'Age_LW_Re_fit': 'Age_LW_Re_fit',
    'ZH_LW_Re_fit': 'ZH_LW_Re_fit',