from sklearn.neighbors import NearestNeighbors


# Redefine the coordinate transformation
def get_coords(df):
    z = df['synthetic_z'].values
    comoving_dist = z * 4285.7  # approximate D_c in Mpc
    
    ra_rad = np.deg2rad(df['synthetic_RA'].values)
    de_rad = np.deg2rad(df['synthetic_DE'].values)
    
    X = comoving_dist * np.cos(de_rad) * np.cos(ra_rad)
    Y = comoving_dist * np.cos(de_rad) * np.sin(ra_rad)
    Z = comoving_dist * np.sin(de_rad)
    
    return np.column_stack((X, Y, Z))


coords = get_coords(df)


# Check distance scale
nn = NearestNeighbors(n_neighbors=10).fit(coords)
distances, _ = nn.kneighbors(coords)
mean_nn_dist = distances.mean(axis=1)


print("Mean Nearest Neighbor Distances (Mpc):")
print(pd.Series(mean_nn_dist).describe())


adaptive_scale_orig = 0.1 * np.median(mean_nn_dist)
print(f"\nOriginal adaptive scale: {adaptive_scale_orig:.4f} Mpc")


# Suggested better scale: 50th percentile of the 25th neighbor
nn25 = NearestNeighbors(n_neighbors=25).fit(coords)
distances25, _ = nn25.kneighbors(coords)
d25 = distances25[:, -1]
print("\nDistance to 25th neighbor (Mpc):")
print(pd.Series(d25).describe())


better_scale = np.percentile(d25, 50)
print(f"\nProposed better scale: {better_scale:.4f} Mpc")
