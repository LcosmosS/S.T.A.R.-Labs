df['DL'] = cosmo.luminosity_distance(df['zsp']).to(u.cm).value
df['L_Ha'] = (df['flux_Ha_corr'] * 4 * np.pi * df['DL']**2 * u.erg / u.s).to(u.L_sun).value
df['log_SFR_Ha_raw'] = np.log10((df['L_Ha'] * sfr_conversion).value)
print(f"NaN in L_Ha: {df['L_Ha'].isna().sum()}")
print(f"NaN in log_SFR_Ha_raw: {df['log_SFR_Ha_raw'].isna().sum()}")

# Add raw fluxes/morpholohicals as features
========================================================================
===================================================================
df['log_flux_Ha'] = np.log10(df['flux_Ha'] + 1e-10)
df['log_flux_Hb'] = np.log10(df['flux_Hb'] + 1e-10)
df['log_flux_OIII_5007'] = np.log10(df['flux_OIII_5007'] + 1e-10)
df['log_flux_NII_6584'] = np.log10(df['flux_NII_6584'] + 1e-10)
df['log_e_flux_Ha'] = np.log10(df['e_flux_Ha'] + 1e-10)

# Compute metallicity
========================================================================
========================================================================
===================
df['log_O3N2_raw'] = np.log10((df['flux_OIII_5007'] / df['flux_Hb']) / (df['flux_NII_6584'] /
