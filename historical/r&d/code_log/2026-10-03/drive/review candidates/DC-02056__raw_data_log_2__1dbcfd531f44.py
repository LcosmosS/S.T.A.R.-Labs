import gudhi
from sklearn.neighbors import NearestNeighbors


# Corrected function snippet to use z_col
def add_physical_local_topology_corrected(df, name, ra_col, de_col, z_col, k=25):
    # Use the passed z_col instead of hardcoded names
    if z_col in df.columns:
        if z_col == 'Vcmb':
            z = df[z_col].values / 3e5
        else:
            z = df[z_col].values
    else:
        z = np.zeros(len(df))
        
    comoving_dist = z * 4285.7
    ra_rad = np.deg2rad(df[ra_col].values)
    de_rad = np.deg2rad(df[de_col].values)
    coords = np.column_stack((
        comoving_dist * np.cos(de_rad) * np.cos(ra_rad),
        comoving_dist * np.cos(de_rad) * np.sin(ra_rad),
        comoving_dist * np.sin(de_rad)
    ))


    # Calculate scale
    nn = NearestNeighbors(n_neighbors=10).fit(coords)
    distances, _ = nn.kneighbors(coords)
    median_nn_dist = np.median(distances.mean(axis=1))
    adaptive_scale = 0.1 * median_nn_dist
    
    # Just return the scale and first few coords to verify
    return adaptive_scale, coords[:5]


scale, sample_coords = add_physical_local_topology_corrected(df, "synth", "synthetic_RA", "synthetic_DE", "synthetic_z")
print(f"Corrected Adaptive Scale: {scale:.2f} Mpc")
print("Sample Coords:")
print(sample_coords)
