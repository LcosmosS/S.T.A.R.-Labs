df['Ha_Hb_observed'] = df['flux_Ha'] / df['flux_Hb']
Ha_Hb_intrinsic = 2.86
k_Ha = 2.468
k_Hb = 3.634
df['A_Ha'] = 2.5 * np.log10(df['Ha_Hb_observed'] / Ha_Hb_intrinsic) * (k_Ha / (k_Hb - k_Ha))
df['flux_Ha_corr'] = df['flux_Ha'] * 10**(0.4 * df['A_Ha'])

# Define cosmology
========================================================================
========================================================================
===========
cosmo = FlatLambdaCDM(H0=70, Om0=0.3)
sfr_conversion = 7.9e-42 * u.Msun / u.yr / u.erg * u.s  # Kennicutt 1998, Salpeter IMF

# Cluster galaxies using RA/Dec and redshift (optimized with parallelization)
========================================================================
=========================
print("initiating galaxy clustering...")
start_time = time.time()

# Convert coordinates to Cartesian for clustering
========================================================================
=====================================================
coords = SkyCoord(ra=df['objra_y']*u.deg, dec=df['objdec']*u.deg,
distance=df['zsp']*cosmo.hubble_distance, frame='icrs')
xyz = coords.cartesian.xyz.value.T  # Shape: (n_rows, 3)

# Build the cKDTree
========================================================================
========================================================================
===========
tree = cKDTree(xyz)
dist_threshold = 1 / cosmo.hubble_distance.value  # ~1 Mpc

# Function to compute neighbors for a chunk of indices
========================================================================
=================================================
def compute_neighbors_chunk(chunk_indices, xyz_data, dist_thr):
    local_tree = cKDTree(xyz_data)  # Rebuild tree for consistency (small overhead)
    return [len(local_tree.query_ball_point(xyz_data[i], r=dist_thr)) - 1 for i in chunk_indices]

# Parallelize the neighbor search
========================================================================
=======================================================================