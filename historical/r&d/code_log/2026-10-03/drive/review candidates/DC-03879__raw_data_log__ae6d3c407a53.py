# Leakage-free photometric + thesis metrics
def add_thesis_features(df):
    df = df.copy()
    # Photometric
    df['flux_gr'] = df.get('Gmag', 0) / (df.get('Jmag', 1) + 1e-8)
    df['pm_mag_proxy'] = np.sqrt(df.get('pmRA', 0)**2 + df.get('pmDE', 0)**2)
    df['mag_ratio'] = df.get('gmag', 0) / (df.get('rmag', 1) + 1e-8)
    # T_cosmo (cosmic time proxy)
    if 'zphot' in df.columns:
        df['T_cosmo'] = 1.0 / (1.0 + df['zphot'])
    elif 'Vcmb' in df.columns:
        df['T_cosmo'] = 1.0 / (1.0 + df['Vcmb'] / 3e5) # approximate redshift from velocity
    else:
        df['T_cosmo'] = 1.0
    # Tully-Fisher proxy (luminosity-velocity)
    if 'Vcmb' in df.columns:
        df['Tully_Fisher'] = df.get('gmag', 0) + 5 * np.log10(df['Vcmb'] / 100.0)
    else:
        df['Tully_Fisher'] = df.get('gmag', 0)
    # Anthropic Principle metric (density fine-tuning proxy)
    if 'V_comove_calibrated' in df.columns and 'rho_scale_calibrated' in df.columns:
        df['Anthropic'] = np.abs(df['rho_scale_calibrated'] - 1.0) # close to critical density
    else:
        df['Anthropic'] = 0.0
    # Force numeric
    for col in ['flux_gr', 'pm_mag_proxy', 'mag_ratio', 'T_cosmo', 'Tully_Fisher', 'Anthropic']:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0).astype(float)
    return df
synth = add_thesis_features(synth)
real1 = add_thesis_features(real1)
real2 = add_thesis_features(real2)
feature_cols = ['flux_gr', 'pm_mag_proxy', 'mag_ratio', 'T_cosmo', 'Tully_Fisher', 'Anthropic']
