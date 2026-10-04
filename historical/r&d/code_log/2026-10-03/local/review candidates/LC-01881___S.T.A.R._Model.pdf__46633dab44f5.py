    df = df_original.copy()
    df['zsp'] = df['nsa_z']
else:
    # Add zsp, umag, gmag, etc. from the merged SDSS dataset
    df = pd.concat([df, sdss_matched[['zsp', 'umag', 'gmag', 'rmag', 'imag', 'zmag', 'e_umag',
'e_gmag', 'e_rmag', 'e_imag', 'e_zmag']]], axis=1)

# II/246: 2MASS Extended Source Catalogue (uses RAJ2000, DEJ2000)
df, twomass_matched = cross_match(df, twomass, 'objra_y', 'objdec', 'RAJ2000', 'DEJ2000',
max_dist_arcsec=10.0)
print(f"After II/246 cross-match: {len(df)} galaxies")
if len(df) > 0:
    df = pd.concat([df, twomass_matched[['Jmag', 'Hmag', 'Kmag', 'e_Jmag', 'e_Hmag',
'e_Kmag']]], axis=1)

# II/356: GAMA DR3 (uses RAJ2000, DEJ2000)
df, gama_matched = cross_match(df, gama, 'objra_y', 'objdec', 'RAJ2000', 'DEJ2000',
max_dist_arcsec=10.0)
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