    df = df.copy()
    
    # --- 1. THE INTRINSIC (Thesis Features) ---
    df['flux_gr'] = df.get('Gmag', 0) / (df.get('Jmag', 1) + 1e-8)
    df['pm_mag_proxy'] = np.sqrt(df.get('pmRA', 0)**2 + df.get('pmDE', 0)**2)
    df['mag_ratio'] = df.get('gmag', 0) / (df.get('rmag', 1) + 1e-8)
    
    if 'Vcmb' in df.columns:
        df['Tully_Fisher'] = df.get('gmag', 0) + 5 * np.log10(df['Vcmb'] / 100.0)
        df['T_cosmo'] = 1.0 / (1.0 + df['Vcmb'] / 3e5)
    else:
        df['Tully_Fisher'] = df.get('gmag', 0)
        df['T_cosmo'] = 1.0 / (1.0 + df.get('zphot', 0))
    
    # --- 2. THE EXTRINSIC (Structural Proxies) ---
    # Betti Connectivity Ratio (The 'Loopiness' Index)
    if 'local_betti_1' in df.columns and 'local_betti_0' in df.columns:
        df['betti_ratio'] = df['local_betti_1'] / (df['local_betti_0'] + 1e-8)
    else:
        df['betti_ratio'] = 0.0


    # Local Anisotropy (Measures the 'stretch' of the filament)
    df['local_anisotropy'] = np.std(dists, axis=1) / (np.mean(dists, axis=1) + 1e-8)
    
    # Density Gradient (Is the galaxy falling into a cluster or a void?)
    neighbor_densities = df['local_density'].values[indices]
    df['density_gradient'] = df['local_density'] - np.mean(neighbor_densities, axis=1)
    
    # Void Proximity Proxy
    df['void_gap'] = dists[:, -1]
    
    # Final numeric cleaning
    cols_to_fix = ['flux_gr', 'pm_mag_proxy', 'mag_ratio', 'Tully_Fisher', 
                   'T_cosmo', 'betti_ratio', 'local_anisotropy', 'density_gradient', 'void_gap']
    
    for col in cols_to_fix:
        df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0).astype(float)
        
    return df
# ====================== 4. ROBUST TOPOLOGY + PERSISTENCE ENTROPY ======================
def persistence_entropy(diag):
    # Only consider finite lifetimes and ignore floating point noise
    lifetimes = [d - b for b, d in diag if np.isfinite(d) and d > b + 1e-8]
    
    if not lifetimes or np.isclose(sum(lifetimes), 0):
        return 0.0
    
    total = sum(lifetimes)
    p = np.array(lifetimes) / total
    return -np.sum(p * np.log(p + 1e-10))


def compute_weighted_topology_worker(i, coords, weights, indices, is_arithmetic=False):
    import gudhi
    import numpy as np


    # 1. Extract local neighborhood
    local_idx = indices[i]
    local_points = coords[local_idx]
    
    # 2. Complex Construction
    if is_arithmetic:
        local_weights = weights[local_idx]
        # AlphaComplex (Power Complex) for weighted arithmetic seeds
        complex_type = gudhi.AlphaComplex(points=local_points, weights=local_weights)
        # FIX: AlphaComplex.create_simplex_tree() takes NO arguments
        st = complex_type.create_simplex_tree()
    else:
        # standard Rips for observational comparison
        # RipsComplex.create_simplex_tree() DOES take max_dimension
        complex_type = gudhi.RipsComplex(
            points=local_points, 
            max_edge_length=np.std(local_points) * 2.0
        )
        st = complex_type.create_simplex_tree(max_dimension=2)
    
    # 3. Persistence Computation
    st.compute_persistence()
    
    # 4. Persistence Entropy (H1 'Heat of the Web')
    def get_entropy(dim):
        intervals = st.persistence_intervals_in_dimension(dim)
        # Filter out infinite intervals for entropy calculation
        lifetimes = [d - b for b, d in intervals if np.isfinite(d) and (d - b) > 0]
        if not lifetimes: 
            return 0.0
        p = np.array(lifetimes) / sum(lifetimes)
        return -np.sum(p * np.log(p + 1e-12))


    # 5. Extract Betti Numbers safely
    # betti_numbers() returns a list [β0, β1, β2, ...]
    bn = st.betti_numbers()
    b0 = bn[0] if len(bn) > 0 else 0
    b1 = bn[1] if len(bn) > 1 else 0
    b2 = bn[2] if len(bn) > 2 else 0
    
    # Return features for the i-th point
    return [float(b0), float(b1), float(b2), float(get_entropy(1))]


def project_arithmetic_to_spatial(df):
    # Ensure numeric types
    df['discriminant'] = pd.to_numeric(df['delta'], errors='coerce') if 'delta' in df.columns else pd.to_numeric(df['discriminant'], errors='coerce')
    df['conductor'] = pd.to_numeric(df['conductor'], errors='coerce')
    df['rank'] = pd.to_numeric(df['rank'], errors='coerce').fillna(0)
    
    # Clean data
    df = df.dropna(subset=['discriminant', 'conductor'])


    # Project into Synthetic Spatial Coordinates
    # RA Proxy: Log-scaled discriminant (Circular)
    df['synthetic_RA'] = np.mod(np.log10(np.abs(df['discriminant']) + 1) * 2 * np.pi, 2 * np.pi)
    # DE Proxy: Log-scaled conductor (Spherical)
    df['synthetic_DE'] = np.mod(np.log10(df['conductor'] + 1) * np.pi, np.pi) - (np.pi / 2)
    # Z Proxy: Rank (Distance/Redshift)
    df['synthetic_z'] = df['rank']
    
    return df


def add_optimized_topology(df, name, ra_col, de_col, z_col, k=25):
    print(f"Computing {name} topology + persistence entropy...")
    
    # 1. Coordinate Transformation
    # Convert redshift to comoving distance (Mpc) for spatial analysis
    z = (df[z_col].values / 3e5) if z_col == 'Vcmb' else df[z_col].values
    comoving_dist = z * 4285.7
    ra_rad = np.deg2rad(df[ra_col].fillna(0).values)
    de_rad = np.deg2rad(df[de_col].fillna(0).values)
    
    coords = np.column_stack((
        comoving_dist * np.cos(de_rad) * np.cos(ra_rad),
        comoving_dist * np.cos(de_rad) * np.sin(ra_rad),
        comoving_dist * np.sin(de_rad)
    ))
    
    # 2. Neighborhood & Scale Calculation (MUST BE BEFORE PARALLEL)
    # We cast k to native int for Sage compatibility
    nn = NearestNeighbors(n_neighbors=int(k)).fit(coords)
    dists, indices = nn.kneighbors(coords)
    
    # Adaptive scale helps normalize the persistence threshold across catalogs
    adaptive_scale = np.percentile(dists[:, -1], 50)
    print(f"   {name} adaptive scale = {adaptive_scale:.2f} Mpc")


    # 3. Arithmetic Weighting Logic
    # Identify if we are processing the Arithmetic (Synth) dataset
    is_arithmetic = 'tda_weight' in df.columns
    weights = df['tda_weight'].values if is_arithmetic else np.ones(len(df))
    
    # 4. Parallel Topological Computation
    # Combined into a single pass for efficiency. 
    # Ensure compute_weighted_topology_worker handles (i, coords, weights, indices, is_arithmetic)
    results = Parallel(n_jobs=-1)(
        delayed(compute_weighted_topology_worker)(i, coords, weights, indices, is_arithmetic)
        for i in range(len(coords))
    )
    
    # 5. Assignment and Metadata Calculation
    res_arr = np.array(results)
    df['local_betti_0'] = res_arr[:, 0]
    df['local_betti_1'] = res_arr[:, 1]
    df['local_betti_2'] = res_arr[:, 2]
    df['persistence_entropy'] = res_arr[:, 3]
    
    # Local density is the average distance to neighbors
    df['local_density'] = dists.mean(axis=1)
    df['normalized_density'] = df['local_density'] / (adaptive_scale + 1e-9)
    df['Anthropic'] = np.abs(df['local_density'] - df['local_density'].median())
    
    # 6. Stratification for Symbolic Regression (PySR)
    if df['persistence_entropy'].nunique() > 1:
        # Create 3 tiers (0, 1, 2) based on entropy for better feature sampling
        df['entropy_strata'] = (df['persistence_entropy'].rank(pct=True, method='first') * 2.99).astype(int)
    else:
        df['entropy_strata'] = 1


    # Final feature expansion
    df = add_comprehensive_proxies(df, coords, dists, indices)
    
    return df


# ====================== EXECUTION ======================
# 1. Load data with Projection applied
synth, real1, real2 = load_and_project_data()


# 2. Add features
synth = add_thesis_features(synth)
real1 = add_thesis_features(real1)
real2 = add_thesis_features(real2, target_col='zphot')


# 1. Project all datasets into the same Geometric Space
synth = project_arithmetic_to_spatial(synth)
real1 = project_arithmetic_to_spatial(real1)


# For real2 (3-selmer), merge with its conductor/delta first if necessary
# Assuming real2 is lmfdb_3selmer_full_pari.csv
# We use the rank from selmer as our 'z'
real2 = real2.rename(columns={'pari_2_selmer_rank': 'rank'}) 
# Note: real2 needs conductor/delta from real1 to project RA/DE
real2 = pd.merge(real2, real1[['label', 'delta', 'conductor']], on='label', how='inner')
real2 = project_arithmetic_to_spatial(real2)


# 2. Compute Topology using CONSISTENT keys
# We no longer use 'Vcmb' or 'RAJ2000' because these are Elliptic Curves, not Galaxies
synth = add_optimized_topology(synth, "synth", "synthetic_RA", "synthetic_DE", "synthetic_z")
real1 = add_optimized_topology(real1, "real1", "synthetic_RA", "synthetic_DE", "synthetic_z")
real2 = add_optimized_topology(real2, "real2", "synthetic_RA", "synthetic_DE", "synthetic_z")


# ====================== FEATURE DEFINITION ======================
# These are the columns that must exist in ALL three dataframes (synth, real1, real2)
common_features = [
    'local_betti_0', 
    'local_betti_1', 
    'local_betti_2', 
    'persistence_entropy',
    'local_density',
    'normalized_density',
    'Anthropic'
]


# Optional: Verify columns exist before imputing to avoid further KeyErrors
for name, df in [("synth", synth), ("real1", real1), ("real2", real2)]:
