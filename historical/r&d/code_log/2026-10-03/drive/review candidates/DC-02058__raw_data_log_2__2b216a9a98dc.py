def add_physical_local_topology(df, name, ra_col, de_col, z_col, k=25):
    # This block ignores z_col!
    if 'zphot' in df.columns:
        z = df['zphot'].values
    elif 'Vcmb' in df.columns:
        z = df['Vcmb'].values / 3e5
    else:
        # Since synthetic_z != zphot, it falls here
        z = np.zeros(len(df)) # <--- ALL COORDINATES BECOME 0,0,0
