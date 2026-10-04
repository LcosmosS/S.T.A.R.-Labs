            print(f"Chunk {i+1} after RA/Dec filter: {len(chunk_filtered)} rows")
            if len(chunk_filtered) == 0:
                continue
            
            _, matched_df2 = cross_match(df1, chunk_filtered, ra_col1, dec_col1, ra_col2, dec_col2, max_dist_arcsec)
            print(f"Chunk {i+1} matches found: {len(matched_df2)}")
            if len(matched_df2) > 0:
                matched_df2_list.append(matched_df2[columns_to_keep])
        
        if len(matched_df2_list) == 0:
            print("No matches found in any chunk.")
            return df1, pd.DataFrame()
        
        matched_df2 = pd.concat(matched_df2_list, ignore_index=True)
        matched_df1 = df1.copy()
        print(f"Final matched_df2 rows: {len(matched_df2)}")
        return matched_df1, matched_df2
    except Exception as e:
        print(f"Error in cross_match_in_chunks: {e}")
        raise
# Store the original DataFrame before cross-matching
df_original = df.copy()# Cross-match with VizieR catalogues
# SDSS merged dataset (V/147 + V/154)
df, sdss_matched = cross_match(df, sdss_merged, 'objra_y', 'objdec', 'RA_ICRS', 'DE_ICRS', max_dist_arcsec=10.0)
print(f"After SDSS cross-match: {len(df)} galaxies")
sdss_columns = ['zsp', 'umag', 'gmag', 'rmag', 'imag', 'zmag', 'e_umag', 'e_gmag', 'e_rmag', 'e_imag', 'e_zmag']
if len(df) == 0:
    print("No matches found with SDSS merged data (V/147 + V/154). Falling back to original data and using nsa_z for redshift.")
    df = df_original.copy()
    df['zsp'] = df['nsa_z']
else:
    # Fill NaN with median for SDSS columns
    print(f"SDSS NaN counts before filling:\n{sdss_matched[sdss_columns].isna().sum()}")
    sdss_matched[sdss_columns] = sdss_matched[sdss_columns].fillna(sdss_matched[sdss_columns].median())
    print(f"SDSS NaN counts after filling:\n{sdss_matched[sdss_columns].isna().sum()}")
    df = pd.concat([df, sdss_matched[sdss_columns]], axis=1)
    print(f"SDSS matches found: {len(sdss_matched)}")
    
    # II/246: 2MASS Extended Source Catalogue
twomass_columns = ['Jmag', 'Hmag', 'Kmag', 'e_Jmag', 'e_Hmag', 'e_Kmag']
df, twomass_matched = cross_match_in_chunks(
    df, "2Mass.csv",
    'objra_y', 'objdec', 'RAJ2000', 'DEJ2000',
    twomass_columns,
    max_dist_arcsec=10.0, chunksize=100000
)
print(f"After II/246 cross-match: {len(df)} galaxies")
if len(df) > 0:
    # Fill NaN with median for 2MASS columns
    print(f"2MASS NaN counts before filling:\n{twomass_matched[twomass_columns].isna().sum()}")
    twomass_matched[twomass_columns] = twomass_matched[twomass_columns].fillna(twomass_matched[twomass_columns].median())
    print(f"2MASS NaN counts after filling:\n{twomass_matched[twomass_columns].isna().sum()}")
    df = pd.concat([df, twomass_matched[twomass_columns]], axis=1)
    
    # II/356: GAMA DR3
gama_columns = ['UmAB', 'BmAB', 'VmAB']
print("Starting GAMA DR3 cross-match...")
df, gama_matched = cross_match_in_chunks(
    df, "II356xmmom41s.csv",
    'objra_y', 'objdec', 'RAJ2000', 'DEJ2000',
    gama_columns,
    max_dist_arcsec=10.0, chunksize=100000
)
print(f"After II/356 cross-match: {len(df)} galaxies")
print(f"gama_matched length: {len(gama_matched)}")
print(f"gama_matched columns: {gama_matched.columns.tolist()}")
if len(gama_matched) > 0 and all(col in gama_matched.columns for col in gama_columns):
    # Fill NaN with median for GAMA columns
    print(f"GAMA NaN counts before filling:\n{gama_matched[gama_columns].isna().sum()}")
    gama_matched[gama_columns] = gama_matched[gama_columns].fillna(gama_matched[gama_columns].median())
    print(f"GAMA NaN counts after filling:\n{gama_matched[gama_columns].isna().sum()}")
    df = pd.concat([df, gama_matched[gama_columns]], axis=1)
else:
    print("No matches found for GAMA DR3 or columns missing, skipping concatenation.")
    # Print columns after cross-matching for debugging
    print("Columns in df after cross-matching:", df.columns.tolist())

# Recompute log_SFR_Ha and metallicity using fluxes from merged_data.csv
df['flux_Ha'] = df['F_Ha_cen']
df['e_flux_Ha'] = df['e_F_Ha_cen']
df['flux_Hb'] = df['flux_Hbeta4861.36_Re_fit']
df['flux_OIII_5007'] = df['flux_[OIII]5006.84_Re_fit']
df['flux_NII_6584'] = df['flux_[NII]6583.45_Re_fit']

# Check for NaN in flux columns and handle them
flux_cols = ['flux_Ha', 'flux_Hb', 'flux_OIII_5007', 'flux_NII_6584', 'e_flux_Ha']
for col in flux_cols:
    nan_count = df[col].isna().sum()
    print(f"NaN count in {col}: {nan_count}")
    if nan_count > 0:
        df[col] = df[col].fillna(df[col].median())

df['Ha_Hb_observed'] = df['flux_Ha'] / df['flux_Hb']  # Line 266 - Moved outside loop
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
print(f"NaN in L_Ha: {df['L_Ha'].isna().sum()}")
print(f"NaN in log_SFR_Ha_raw: {df['log_SFR_Ha_raw'].isna().sum()}")

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

if 'Jmag' in df.columns:  # Line 298 - Moved to new line, dedented
    df['color_JK'] = df['Jmag'] - df['Kmag']
    df['e_color_JK'] = np.sqrt(df['e_Jmag']**2 + df['e_Kmag']**2)
    
# Drop rows with missing target or excessive NaNs, then fill remaining NaNs
df = df.dropna(subset=["log_SFR_Ha_raw"])
df = df.dropna(axis=0, thresh=int(0.5 * df.shape[1]))  # 50% non-NaN

# Step 1: Cosmo-Rank Construction
gz_df = df.copy()
morph_cols = ['P(CD)', 'P(E)', 'P(S0)', 'P(Sa)', 'P(Sab)', 'P(Sb)', 'P(Sbc)', 
              'P(Sc)', 'P(Scd)', 'P(Sd)', 'P(Sdm)', 'P(Sm)', 'P(Irr)']
gz_df['morph_sum'] = gz_df[morph_cols].sum(axis=1)
gz_df['Num_w'] = gz_df['conf_prob']
scaler_rank = MinMaxScaler()
