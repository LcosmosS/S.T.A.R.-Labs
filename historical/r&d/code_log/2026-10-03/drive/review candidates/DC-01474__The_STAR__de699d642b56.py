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


# Diagnostics for L_cosmo_s_* features ================================================================================================================================
print(f"cosmo_rank: mean={df['cosmo_rank'].mean():.4f}, std={df['cosmo_rank'].std():.4f}")
for s in [0.5, 1.0, 1.5, 2.0]:
    col = f'L_cosmo_s_{s:.1f}'
    print(f"{col}: mean={df[col].mean():.4f}, std={df[col].std():.4f}, NaN={df[col].isna().sum()}, Inf={np.isinf(df[col]).sum()}")


# Feature engineering with proper cosmic measurements =================================================================================================================
df['log_Mass'] = df['log_Mass_gas'] 


# Check for missing columns and compute if necessary ==================================================================================================================
required_cols = {
    'SpecObj': 'SpecObj',
    'OH_O3N2_cen': 'OH_O3N2_cen',
    'OH_T04_cen': 'OH_T04_cen',
    'Av_gas_Re': 'Av_gas_Re',
    'vel_disp_Ha_cen': 'vel_disp_Ha_cen',
    'Sigma_Mass_Re': 'Sigma_Mass_Re',
    'Age_LW_Re_fit': 'Age_LW_Re_fit',
    'ZH_LW_Re_fit': 'ZH_LW_Re_fit',
    'EW_Ha_cen': 'EW_Ha_cen',
    'stellar_mass': 'stellar_mass',
    'Re_kpc': 'Re_kpc',
    'redshift': 'redshift',
    'cosmo_rank_L': 'cosmo_rank'
}
for col, fallback in required_cols.items():
    if col not in df.columns:
        if col == 'Av_gas_Re':
            if 'AV50' in df.columns and 'A0' in df.columns:
                df['Av_gas_Re'] = df['AV50'].fillna(df['A0']).fillna(0)
            elif 'AV50' in df.columns:
                df['Av_gas_Re'] = df['AV50'].fillna(0)
            elif 'A0' in df.columns:
                df['Av_gas_Re'] = df['A0'].fillna(0)
            else:
                df['Av_gas_Re'] = 0
            print("Assigned Av_gas_Re from AV50/A0")
        elif col == 'Age_LW_Re_fit':
            df['Age_LW_Re_fit'] = df.get('Age-Flame', 0)
            print("Assigned Age_LW_Re_fit from Age-Flame")
        elif col == 'ZH_LW_Re_fit':
            df['ZH_LW_Re_fit'] = df.get('met50', 0)
            print("Assigned ZH_LW_Re_fit from met50")
        elif col == 'cosmo_rank_L':
            df['cosmo_rank_L'] = df.get('cosmo_rank', 0.5)
            print("Assigned cosmo_rank_L from cosmo_rank")
        elif fallback:
            df[col] = df.get(fallback, np.nan)
            print(f"Warning: {col} not found. Using {fallback} as fallback.")
        else:
            print(f"Warning: {col} not found. Setting to 0.")
            df[col] = 0


# Feature engineering block with cosmic adjustments ===================================================================================================================
print(f"Memory usage before feature engineering: {df.memory_usage().sum() / 1024**2:.2f} MB")


# Precompute constants and reusable series to avoid redundant calculations ============================================================================================
logMass = df['logMass'].values  # Convert to NumPy array for efficiency
cosmo_rank = df['cosmo_rank'].values
L_cosmo_s1 = df['L_cosmo_s_1.0'].values


# Dictionary to store new features as NumPy arrays ====================================================================================================================
new_features_dict = {}


# Compute new features using NumPy for efficiency =====================================================================================================================
new_features_dict['mass_metallicity'] = logMass * df['OH_O3N2_raw'].values
new_features_dict['dust_metallicity'] = df['Av_gas_Re'].values * df.get('OH_T04_cen', 0).values
new_features_dict['disp_mass_ratio'] = df['vel_disp_Ha_cen'].values / (df['Sigma_Mass_Re'].values + 1e-5)
new_features_dict['age_metallicity'] = df['Age_LW_Re_fit'].values * df['ZH_LW_Re_fit'].values
new_features_dict['sqrt_Re_kpc'] = np.sqrt(df['Re_kpc'].values + 1e-5)
new_features_dict['BSD_likelihood'] = logMass * df['OH_O3N2_raw'].values / (df['Av_gas_Re'].values + df['Age_LW_Re_fit'].values + 1e-5)
new_features_dict['cosmo_rank_mass'] = cosmo_rank * logMass
new_features_dict['L_cosmo_s1_mass'] = L_cosmo_s1 * logMass
new_features_dict['cosmo_rank_EW'] = cosmo_rank * df['EW_Ha_cen'].values
new_features_dict['L_cosmo_s1_EW'] = L_cosmo_s1 * df['EW_Ha_cen'].values
new_features_dict['cosmo_rank_scaled'] = cosmo_rank * 20
new_features_dict['L_cosmo_s1_scaled'] = L_cosmo_s1 * 20
new_features_dict['L_cosmo_s1_metallicity'] = L_cosmo_s1 * df['OH_O3N2_raw'].values


# Impute new features one at a time to reduce memory overhead =========================================================================================================
new_features = [
    "mass_metallicity", "dust_metallicity", "disp_mass_ratio", "age_metallicity",
    "sqrt_Re_kpc", "BSD_likelihood", "cosmo_rank_mass", "L_cosmo_s1_mass",
    "cosmo_rank_EW", "L_cosmo_s1_EW", "cosmo_rank_scaled", "L_cosmo_s1_scaled",
    "L_cosmo_s1_metallicity"
]


for feature in new_features:
    # Replace inf with NaN and compute median -----------------------------------------------------
    arr = np.where(np.isfinite(new_features_dict[feature]), new_features_dict[feature], np.nan)
    median_val = np.nanmedian(arr)
    # Impute NaN with median ----------------------------------------------------------------------
    new_features_dict[feature] = np.where(np.isnan(arr), median_val, arr)
    # Assign to DataFrame -------------------------------------------------------------------------
    df[feature] = new_features_dict[feature]
    del new_features_dict[feature]


# Free memory of precomputed arrays ---------------------------------------------------------------
