def add_physical_local_topology(df, name, ra_col, de_col, z_col, k=25):
    # FIX: Use the variable z_col instead of hardcoded strings
    if z_col in df.columns:
        if z_col == 'Vcmb':
            z = df[z_col].values / 3e5 # Convert velocity to redshift
        else:
            z = df[z_col].values # synthetic_z is already redshift
    else:
        z = np.zeros(len(df))


    comoving_dist = z * 4285.7  # D_c in Mpc (H0=70)
    
    ra_rad = np.deg2rad(df[ra_col].values)
    de_rad = np.deg2rad(df[de_col].values)


    X = comoving_dist * np.cos(de_rad) * np.cos(ra_rad)
    Y = comoving_dist * np.cos(de_rad) * np.sin(ra_rad)
    Z = comoving_dist * np.sin(de_rad)
    coords = np.column_stack((X, Y, Z))


    # SCALE FIX: 0.1 * median is often too small for Betti-1 (holes).
    # Try using the 50th percentile of the k-th neighbor distance.
    nn = NearestNeighbors(n_neighbors=k).fit(coords)
    distances, indices = nn.kneighbors(coords)
    
    # This captures the typical "bridge" distance to form loops
    adaptive_scale = np.percentile(distances[:, -1], 50) 
    print(f"   {name} corrected adaptive scale = {adaptive_scale:.2f} Mpc")
    
    # ... rest of GUDHI loop ...
