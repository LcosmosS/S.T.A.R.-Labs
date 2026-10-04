from scipy.spatial import cKDTree


# Load VizieR data
sdss_data = pd.read_csv("sdss_dr16_spec.csv")  # Update with actual path


# Convert coordinates to radians
def deg_to_rad(df, ra_col, dec_col):
    df['ra_rad'] = np.radians(df[ra_col])
    df['dec_rad'] = np.radians(df[dec_col])
    return df


df = deg_to_rad(df, 'objra_y', 'objdec')
sdss_data = deg_to_rad(sdss_data, 'RA', 'Dec')


# Cross-match
coords1 = np.array([df['ra_rad'], df['dec_rad']]).T
coords2 = np.array([sdss_data['ra_rad'], sdss_data['dec_rad']]).T
tree = cKDTree(coords2)
max_dist = np.radians(1.0 / 3600.0)  # 1 arcsec
dist, idx = tree.query(coords1, k=1, distance_upper_bound=max_dist)
matched = dist < max_dist
df_matched = df[matched].copy()
sdss_matched = sdss_data.iloc[idx[matched]].copy()
df_matched = df_matched.reset_index(drop=True)
sdss_matched = sdss_matched.reset_index(drop=True)
df = pd.concat([df_matched, sdss_matched[['specz', 'flux_Ha', 'flux_Hb', 'flux_OIII_5007', 'flux_NII_6584', 'e_flux_Ha']]], axis=1)
   * print(f"Number of galaxies after cross-match: {len(df)}")
