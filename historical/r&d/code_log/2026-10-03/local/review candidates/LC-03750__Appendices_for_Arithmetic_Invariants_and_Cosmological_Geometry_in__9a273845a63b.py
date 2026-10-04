    return df_analysis

def clean_and_prepare_data(df):
    df_clean = df.dropna(subset=['virial_energy_j', 'discriminant', 'logmass',
'distance_mpc', 'density_kg_m3']).copy()
    df_clean = df_clean[np.isfinite(df_clean['discriminant']) &
(df_clean['discriminant'] != 0)]

    # --- LOG-TRANSFORM STABILITY ANCHOR ---
    # We work with absolute values as energy is negative and discriminant can be.
    df_clean['log_abs_virial_energy'] = np.log10(np.abs(df_clean['virial_energy_j']))
    df_clean['log_abs_discriminant'] = np.log10(np.abs(df_clean['discriminant']))

    # Now, calculate K and clean based on the stable log values
