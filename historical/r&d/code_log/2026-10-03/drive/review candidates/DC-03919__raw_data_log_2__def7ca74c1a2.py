# ====================== THESIS METRICS ======================
def add_thesis_features(df):
    df = df.copy()
    df['flux_gr'] = df.get('Gmag', 0) / (df.get('Jmag', 1) + 1e-8)
    df['pm_mag_proxy'] = np.sqrt(df.get('pmRA', 0)**2 + df.get('pmDE', 0)**2)
    df['mag_ratio'] = df.get('gmag', 0) / (df.get('rmag', 1) + 1e-8)
    if 'zphot' in df.columns:
        df['T_cosmo'] = 1.0 / (1.0 + df['zphot'])
    elif 'Vcmb' in df.columns:
        df['T_cosmo'] = 1.0 / (1.0 + df['Vcmb'] / 3e5)
    else:
        df['T_cosmo'] = 1.0
    if 'Vcmb' in df.columns:
        df['Tully_Fisher'] = df.get('gmag', 0) + 5 * np.log10(df['Vcmb'] / 100.0)
    else:
        df['Tully_Fisher'] = df.get('gmag', 0)
    for col in ['flux_gr', 'pm_mag_proxy', 'mag_ratio', 'T_cosmo', 'Tully_Fisher']:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0).astype(float)
    return df


synth = add_thesis_features(synth)
real1 = add_thesis_features(real1)
real2 = add_thesis_features(real2)


# ====================== PHYSICAL TOPOLOGY ======================
def add_physical_local_topology(df, name, ra_col, de_col, z_col, k=25):
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
    nn = NearestNeighbors(n_neighbors=k).fit(coords)
    distances, _ = nn.kneighbors(coords)
    adaptive_scale = np.percentile(distances[:, -1], 50)
    print(f"   {name} adaptive scale = {adaptive_scale:.2f} Mpc (k={k})")
    df[name + '_local_density'] = distances.mean(axis=1)
    df['Anthropic'] = np.abs(df[name + '_local_density'] - np.median(df[name + '_local_density']))
    local_betti = np.zeros((len(coords), 3), dtype=int)
    for i in range(len(coords)):
        neigh_idx = nn.kneighbors(coords[i].reshape(1, -1), return_distance=False)[0]
        neigh_points = coords[neigh_idx]
        rips = gudhi.RipsComplex(points=neigh_points, max_edge_length=adaptive_scale)
        st = rips.create_simplex_tree(max_dimension=2)
        st.compute_persistence()
        betti = st.betti_numbers()
        for j in range(3):
            local_betti[i, j] = betti[j] if len(betti) > j else 0
    for i in range(3):
        df[name + f'_local_betti_{i}'] = local_betti[:, i]
    print(f"   {name} per-galaxy local Betti_0/1/2 computed")
    return df


print("\nComputing topology...")
real1 = add_physical_local_topology(real1, "real1", "RAJ2000", "DEJ2000", "Vcmb")
real2 = add_physical_local_topology(real2, "real2", "RAdeg", "DEdeg", "zphot")
synth = add_physical_local_topology(synth, "synth", "synthetic_RA", "synthetic_DE", "synthetic_z")


# ====================== KNN IMPUTATION (physically consistent) ======================
print("\n🧼 KNN imputation on all features (k=10, distance-weighted)...")
imputer = KNNImputer(n_neighbors=10, weights='distance')
base_cols = ['flux_gr', 'pm_mag_proxy', 'mag_ratio', 'T_cosmo', 'Tully_Fisher', 'Anthropic']


for df, name in [(synth, "synth"), (real1, "real1"), (real2, "real2")]:
