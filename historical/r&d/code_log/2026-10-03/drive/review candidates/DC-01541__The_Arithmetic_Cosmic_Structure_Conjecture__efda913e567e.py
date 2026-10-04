def spatial_match(df1, df2, max_sep=2.0):
    coords1 = np.deg2rad(np.vstack([df1['ra'], df1['dec']]).T)
    coords2 = np.deg2rad(np.vstack([df2['ra'], df2['dec']]).T)
    tree = cKDTree(coords2)
    dists, idxs = tree.query(coords1, distance_upper_bound=np.radians(max_sep / 3600))
    match_mask = dists != np.inf
    return df1[match_mask], df2.iloc[idxs[match_mask]]
