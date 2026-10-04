    return df_analysis

def clean_and_prepare_data(df):
    df_clean = df.dropna(subset=['virial_energy_j', 'discriminant', 'logmass',
'distance_mpc', 'density_kg_m3']).copy()
    df_clean = df_clean[np.isfinite(df_clean['discriminant']) &
(df_clean['discriminant'] != 0)]
    df_clean['scaling_constant_K'] = df_clean['virial_energy_j'] /
