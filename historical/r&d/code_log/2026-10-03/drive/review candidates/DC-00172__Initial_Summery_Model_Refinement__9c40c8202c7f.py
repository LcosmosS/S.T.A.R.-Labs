# After loading your dataset
# Load VizieR V/154 data (assuming you downloaded it as 'sdss_dr16_spec.csv')
sdss_data = pd.read_csv("sdss_dr16_spec.csv")


# Cross-match based on coordinates (RA, Dec)
# Your dataset uses 'objra_y', 'objdec'; V/154 uses 'RA', 'Dec'
from scipy.spatial import cKDTree


# Convert coordinates to radians for spherical distance
def deg_to_rad(df, ra_col, dec_col):
    df['ra_rad'] = np.radians(df[ra_col])
    df['dec_rad'] = np.radians(df[dec_col])
    return df


df = deg_to_rad(df, 'objra_y', 'objdec')
sdss_data = deg_to_rad(sdss_data, 'RA', 'Dec')


# Create coordinate arrays for KDTree
coords1 = np.array([df['ra_rad'], df['dec_rad']]).T
coords2 = np.array([sdss_data['ra_rad'], sdss_data['dec_rad']]).T


# Build KDTree for efficient nearest-neighbor search
tree = cKDTree(coords2)


# Find nearest neighbors within a threshold (e.g., 1 arcsec = 1/3600 degrees)
max_dist = np.radians(1.0 / 3600.0)  # 1 arcsec in radians
dist, idx = tree.query(coords1, k=1, distance_upper_bound=max_dist)


# Create a mask for matches
matched = dist < max_dist
df_matched = df[matched].copy()
sdss_matched = sdss_data.iloc[idx[matched]].copy()


# Merge the matched data
df_matched = df_matched.reset_index(drop=True)
sdss_matched = sdss_matched.reset_index(drop=True)
df_merged = pd.concat([df_matched, sdss_matched[['specz', 'flux_Ha', 'flux_Hb', 'flux_OIII_5007', 'flux_NII_6584', 'e_flux_Ha']]], axis=1)


# Update df to the matched subset
df = df_merged
print(f"Number of galaxies after cross-match: {len(df)}")
