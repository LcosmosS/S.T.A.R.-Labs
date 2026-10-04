    else:
        df['Anthropic'] = 0.0

    if target_col != 'zphot' and 'zphot' in df.columns:
        df['T_cosmo'] = 1.0 / (1.0 + df['zphot'])
    elif 'Vcmb' in df.columns:
        df['T_cosmo'] = 1.0 / (1.0 + df['Vcmb'] / 3e5)
    else:
        df['T_cosmo'] = 1.0

    for col in ['flux_gr', 'pm_mag_proxy', 'mag_ratio', 'Tully_Fisher', 'Anthropic', 'T_cosmo']:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0).astype(float)
    return df

def add_comprehensive_proxies(df, coords, dists, indices, target_col=None):
    """
    Combines intrinsic photometric proxies with extrinsic structural geometry.
