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
# ====================== 4. ROBUST TOPOLOGY + PERSISTENCE ENTROPY
======================
def persistence_entropy(diag):
    # Only consider finite lifetimes and ignore floating point noise
    lifetimes = [d - b for b, d in diag if np.isfinite(d) and d > b + 1e-8]

    if not lifetimes or np.isclose(sum(lifetimes), 0):
        return 0.0

    total = sum(lifetimes)
    p = np.array(lifetimes) / total
    return -np.sum(p * np.log(p + 1e-10))

def compute_topology_worker(i, coords, indices, adaptive_scale):
    local_points = coords[indices[i]]
    rips = gudhi.RipsComplex(points=local_points, max_edge_length=adaptive_scale)
    st = rips.create_simplex_tree(max_dimension=2)
    st.compute_persistence()
    betti = st.betti_numbers()
    h1_pers = st.persistence_intervals_in_dimension(1)
    entropy = persistence_entropy(h1_pers)
    return [betti[0] if len(betti) > 0 else 0,
            betti[1] if len(betti) > 1 else 0,
            betti[2] if len(betti) > 2 else 0,
