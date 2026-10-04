    on='objID',
    how='outer',
    suffixes=('_dr16', '_dr12')
)


# Combine columns, preferring DR16 values where available, otherwise use DR12
sdss_merged['RA_ICRS'] = sdss_merged['RA_ICRS_dr16'].combine_first(sdss_merged['RA_ICRS_dr12'])
sdss_merged['DE_ICRS'] = sdss_merged['DE_ICRS_dr16'].combine_first(sdss_merged['DE_ICRS_dr12'])
sdss_merged['zsp'] = sdss_merged['zsp_dr16'].combine_first(sdss_merged['zsp_dr12'])
sdss_merged['umag'] = sdss_merged['umag_dr16'].combine_first(sdss_merged['umag_dr12'])
sdss_merged['gmag'] = sdss_merged['gmag_dr16'].combine_first(sdss_merged['gmag_dr12'])
sdss_merged['rmag'] = sdss_merged['rmag_dr16'].combine_first(sdss_merged['rmag_dr12'])
sdss_merged['imag'] = sdss_merged['imag_dr16'].combine_first(sdss_merged['imag_dr12'])
sdss_merged['zmag'] = sdss_merged['zmag_dr16'].combine_first(sdss_merged['zmag_dr12'])
sdss_merged['e_umag'] = sdss_merged['e_umag_dr16'].combine_first(sdss_merged['e_umag_dr12'])
sdss_merged['e_gmag'] = sdss_merged['e_gmag_dr16'].combine_first(sdss_merged['e_gmag_dr12'])
sdss_merged['e_rmag'] = sdss_merged['e_rmag_dr16'].combine_first(sdss_merged['e_rmag_dr12'])
sdss_merged['e_imag'] = sdss_merged['e_imag_dr16'].combine_first(sdss_merged['e_imag_dr12'])
sdss_merged['e_zmag'] = sdss_merged['e_zmag_dr16'].combine_first(sdss_merged['e_zmag_dr12'])


# Drop the intermediate columns
sdss_merged = sdss_merged[['objID', 'RA_ICRS', 'DE_ICRS', 'zsp', 'umag', 'gmag', 'rmag', 'imag', 'zmag', 'e_umag', 'e_gmag', 'e_rmag', 'e_imag', 'e_zmag']]


# Save the merged dataset for future use
sdss_merged.to_csv("sdss_merged.csv", index=False)
print(f"Merged SDSS dataset created with {len(sdss_merged)} rows.")


# Load the other datasets
twomass = pd.read_csv("2Mass.csv")  # II/246: 2MASS Extended Source Catalogue
gama = pd.read_csv("II356xmmom41s.csv")  # II/356: GAMA DR3


# Print columns for debugging
print("Columns in merged_data.csv:", df.columns.tolist())
print("Columns in sdss_merged (V/147 + V/154):", sdss_merged.columns.tolist())
print("Columns in twomass (II/246):", twomass.columns.tolist())
print("Columns in gama (II/356):", gama.columns.tolist())


# Function to clean DataFrame by removing rows with NaN or inf in RA/Dec columns
def clean_coordinates(df, ra_col, dec_col):
    initial_len = len(df)
    # Check for NaN or inf in RA and Dec columns
    mask = (
        df[ra_col].notna() & df[dec_col].notna() &  # Not NaN
        np.isfinite(df[ra_col]) & np.isfinite(df[dec_col])  # Not inf
    )
    df_cleaned = df[mask].copy()
    print(f"Removed {initial_len - len(df_cleaned)} rows from DataFrame due to NaN or inf in {ra_col} or {dec_col}")
    # Print RA/Dec ranges for debugging
    if len(df_cleaned) > 0:
        print(f"RA range in {ra_col}: {df_cleaned[ra_col].min():.4f} to {df_cleaned[ra_col].max():.4f}")
        print(f"Dec range in {dec_col}: {df_cleaned[dec_col].min():.4f} to {df_cleaned[dec_col].max():.4f}")
    else:
        print(f"No valid RA/Dec data after cleaning in {ra_col}/{dec_col}")
    return df_cleaned


# Cross-match function
def deg_to_rad(df, ra_col, dec_col):
    try:
        df['ra_rad'] = np.radians(df[ra_col])
        df['dec_rad'] = np.radians(df[dec_col])
        return df
    except KeyError as e:
        print(f"KeyError in deg_to_rad: {e}")
        print(f"Available columns in DataFrame: {df.columns.tolist()}")
        raise


def cross_match(df1, df2, ra_col1, dec_col1, ra_col2, dec_col2, max_dist_arcsec=10.0):
    try:
        # Clean DataFrames to remove rows with NaN or inf in RA/Dec
        df1_cleaned = clean_coordinates(df1, ra_col1, dec_col1)
        df2_cleaned = clean_coordinates(df2, ra_col2, dec_col2)


        # Check if either DataFrame is empty after cleaning
        if len(df1_cleaned) == 0 or len(df2_cleaned) == 0:
            print("One of the DataFrames is empty after cleaning. Cannot perform cross-match.")
            return df1_cleaned, pd.DataFrame()


        # Convert degrees to radians
        df1_cleaned = deg_to_rad(df1_cleaned, ra_col1, dec_col1)
        df2_cleaned = deg_to_rad(df2_cleaned, ra_col2, dec_col2)


        # Create coordinate arrays
        coords1 = np.array([df1_cleaned['ra_rad'], df1_cleaned['dec_rad']]).T
        coords2 = np.array([df2_cleaned['ra_rad'], df2_cleaned['dec_rad']]).T


        # Perform cross-match using cKDTree
        tree = cKDTree(coords2)
        max_dist = np.radians(max_dist_arcsec / 3600.0)
        dist, idx = tree.query(coords1, k=1, distance_upper_bound=max_dist)


        # Filter matches within the maximum distance
        matched = dist < max_dist
        df1_matched = df1_cleaned[matched].copy()
        df2_matched = df2_cleaned.iloc[idx[matched]].copy()


        # Reset indices
        df1_matched = df1_matched.reset_index(drop=True)
        df2_matched = df2_matched.reset_index(drop=True)


        # Print sample matches for debugging
        if len(df1_matched) > 0:
            print("Sample matches (first 5):")
            for i in range(min(5, len(df1_matched))):
                print(f"Match {i+1}: {ra_col1}={df1_matched[ra_col1].iloc[i]:.4f}, {dec_col1}={df1_matched[dec_col1].iloc[i]:.4f} "
                      f"matched to {ra_col2}={df2_matched[ra_col2].iloc[i]:.4f}, {dec_col2}={df2_matched[dec_col2].iloc[i]:.4f} "
                      f"(distance={(dist[matched][i] * 3600 * 180 / np.pi):.2f} arcsec)")
        else:
            print("No matches found within the specified radius.")


        return df1_matched, df2_matched
    except KeyError as e:
        print(f"KeyError in cross_match: {e}")
        print(f"df1 columns: {df1.columns.tolist()}")
        print(f"df2 columns: {df2.columns.tolist()}")
        raise
    except Exception as e:
        print(f"Error in cross_match: {e}")
        raise


# Store the original DataFrame before cross-matching
df_original = df.copy()


# Cross-match with VizieR catalogues
# SDSS merged dataset (V/147 + V/154, uses RA_ICRS, DE_ICRS)
df, sdss_matched = cross_match(df, sdss_merged, 'objra_y', 'objdec', 'RA_ICRS', 'DE_ICRS', max_dist_arcsec=10.0)
print(f"After SDSS cross-match: {len(df)} galaxies")


# Check if cross-match succeeded; if not, fall back to original DataFrame
if len(df) == 0:
    print("No matches found with SDSS merged data (V/147 + V/154). Falling back to original data and using nsa_z for redshift.")
    df = df_original.copy()
    df['zsp'] = df['nsa_z']
else:
    # Add zsp, umag, gmag, etc. from the merged SDSS dataset
    df = pd.concat([df, sdss_matched[['zsp', 'umag', 'gmag', 'rmag', 'imag', 'zmag', 'e_umag', 'e_gmag', 'e_rmag', 'e_imag', 'e_zmag']]], axis=1)


# II/246: 2MASS Extended Source Catalogue (uses RAJ2000, DEJ2000)
df, twomass_matched = cross_match(df, twomass, 'objra_y', 'objdec', 'RAJ2000', 'DEJ2000', max_dist_arcsec=10.0)
print(f"After II/246 cross-match: {len(df)} galaxies")
if len(df) > 0:
    df = pd.concat([df, twomass_matched[['Jmag', 'Hmag', 'Kmag', 'e_Jmag', 'e_Hmag', 'e_Kmag']]], axis=1)


# II/356: GAMA DR3 (uses RAJ2000, DEJ2000)
df, gama_matched = cross_match(df, gama, 'objra_y', 'objdec', 'RAJ2000', 'DEJ2000', max_dist_arcsec=10.0)
print(f"After II/356 cross-match: {len(df)} galaxies")
if len(df) > 0:
    df = pd.concat([df, gama_matched[['UmAB', 'BmAB', 'VmAB']]], axis=1)


# Recompute log_SFR_Ha and metallicity using fluxes from merged_data.csv
df['flux_Ha'] = df['F_Ha_cen']  # Use F_Ha_cen as flux_Ha
df['e_flux_Ha'] = df['e_F_Ha_cen']
df['flux_Hb'] = df['flux_Hbeta4861.36_Re_fit']
df['flux_OIII_5007'] = df['flux_[OIII]5006.84_Re_fit']
df['flux_NII_6584'] = df['flux_[NII]6583.45_Re_fit']


# Check for NaN in flux columns and handle them
flux_cols = ['flux_Ha', 'flux_Hb', 'flux_OIII_5007', 'flux_NII_6584', 'e_flux_Ha']
for col in flux_cols:
    nan_count = df[col].isna().sum()
    print(f"NaN count in {col}: {nan_count}")
    # Replace NaN with median for flux columns
    if nan_count > 0:
        df[col] = df[col].fillna(df[col].median())


df['Ha_Hb_observed'] = df['flux_Ha'] / df['flux_Hb']
Ha_Hb_intrinsic = 2.86
k_Ha = 2.468
k_Hb = 3.634
df['A_Ha'] = 2.5 * np.log10(df['Ha_Hb_observed'] / Ha_Hb_intrinsic) * (k_Ha / (k_Hb - k_Ha))
df['flux_Ha_corr'] = df['flux_Ha'] * 10**(0.4 * df['A_Ha'])
H0 = 70  # km/s/Mpc
c = 3e5  # km/s
df['DL'] = (c * df['zsp'] / H0) * 3.0856e24  # cm, using zsp
df['L_Ha'] = df['flux_Ha_corr'] * 4 * np.pi * df['DL']**2  # erg/s
df['log_SFR_Ha_raw'] = np.log10(df['L_Ha'] * 7.9e-42)  # M_sun/yr
df['log_O3N2_raw'] = np.log10((df['flux_OIII_5007'] / df['flux_Hb']) / (df['flux_NII_6584'] / df['flux_Ha']))
df['OH_O3N2_raw'] = 8.533 - 0.214 * df['log_O3N2_raw']


# Add raw fluxes as features
df['log_flux_Ha'] = np.log10(df['flux_Ha'] + 1e-10)
df['log_flux_Hb'] = np.log10(df['flux_Hb'] + 1e-10)
df['log_flux_OIII_5007'] = np.log10(df['flux_OIII_5007'] + 1e-10)
df['log_flux_NII_6584'] = np.log10(df['flux_NII_6584'] + 1e-10)
df['log_e_flux_Ha'] = np.log10(df['e_flux_Ha'] + 1e-10)


# Add photometric colors (if available)
if 'umag' in df.columns:
    df['color_ug'] = df['umag'] - df['gmag']
    df['color_gr'] = df['gmag'] - df['rmag']
    df['color_ri'] = df['rmag'] - df['imag']
    df['color_iz'] = df['imag'] - df['zmag']
    df['e_color_ug'] = np.sqrt(df['e_umag']**2 + df['e_gmag']**2)
    df['e_color_gr'] = np.sqrt(df['e_gmag']**2 + df['e_rmag']**2)


# Add 2MASS colors (if available)
if 'Jmag' in df.columns:
    df['color_JK'] = df['Jmag'] - df['Kmag']
    df['e_color_JK'] = np.sqrt(df['e_Jmag']**2 + df['e_Kmag']**2)


# Drop rows with missing target or excessive NaNs
df = df.dropna(subset=["log_SFR_Ha"])
df = df.dropna(axis=0, thresh=int(0.8 * df.shape[1]))
df.fillna(df.median(numeric_only=True), inplace=True)


# Step 1: Cosmo-Rank Construction
gz_df = df.copy()
morph_cols = ['P(CD)', 'P(E)', 'P(S0)', 'P(Sa)', 'P(Sab)', 'P(Sb)', 'P(Sbc)', 
              'P(Sc)', 'P(Scd)', 'P(Sd)', 'P(Sdm)', 'P(Sm)', 'P(Irr)']
gz_df['morph_sum'] = gz_df[morph_cols].sum(axis=1)
gz_df['Num_w'] = gz_df['conf_prob']
scaler_rank = MinMaxScaler()
