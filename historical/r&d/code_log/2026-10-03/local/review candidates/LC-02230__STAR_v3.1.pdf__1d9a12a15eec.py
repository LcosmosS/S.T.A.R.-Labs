    z = (df[z_col].values / 3e5) if z_col == 'Vcmb' else df[z_col].values
    comoving_dist = z * 4285.7
    ra_rad = np.deg2rad(df[ra_col].fillna(0).values)
    de_rad = np.deg2rad(df[de_col].fillna(0).values)
    coords = np.column_stack((
        comoving_dist * np.cos(de_rad) * np.cos(ra_rad),
        comoving_dist * np.cos(de_rad) * np.sin(ra_rad),
        comoving_dist * np.sin(de_rad)
    ))

    # 2. Neighborhood & Scale Calculation
    nn = NearestNeighbors(n_neighbors=k).fit(coords)
    dists, indices = nn.kneighbors(coords)
    adaptive_scale = np.percentile(dists[:, -1], 50)
    print(f"   {name} adaptive scale = {adaptive_scale:.2f} Mpc")

    # 3. Parallel Topological Computation
    results = Parallel(n_jobs=-1)(
        delayed(compute_topology_worker)(i, coords, indices, adaptive_scale)
        for i in range(len(coords))
    )

    # 4. Assignment to DataFrame
    res_arr = np.array(results)
    df['local_betti_0'] = res_arr[:, 0]
    df['local_betti_1'] = res_arr[:, 1]
    df['local_betti_2'] = res_arr[:, 2]
    df['persistence_entropy'] = res_arr[:, 3]
    df['local_density'] = dists.mean(axis=1)

    # 5. NOW we can calculate normalized metrics
    df['normalized_density'] = df['local_density'] / adaptive_scale
    df['Anthropic'] = np.abs(df['local_density'] - df['local_density'].median())

    # 6. Stratification and Proxies
    if df['persistence_entropy'].nunique() > 1:
        df['entropy_strata'] = (df['persistence_entropy'].rank(pct=True, method='first') *
