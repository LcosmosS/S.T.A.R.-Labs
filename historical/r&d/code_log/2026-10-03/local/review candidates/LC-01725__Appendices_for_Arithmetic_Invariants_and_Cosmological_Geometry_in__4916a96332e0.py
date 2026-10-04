def generate_elliptic_curves(num_curves):
    curves = [generate_curve(i) for i in range(1, num_curves + 1)]
    return pd.DataFrame([c for c in curves if c is not None])

# Bin by generator type
def bin_by_generator(df_curves):
    bins = df_curves.groupby(['gen_type', 'rational_gen'])
    bin_summary = {name: len(group) for name, group in bins}
    logger.info(f"Bin summary: {bin_summary}")
    with open('ucf_analysis.txt', 'a') as f:
        f.write(f"Bin summary: {bin_summary}\n")
    return bin_summary

# Projection Φ
def compute_projection(df_curves):
    df = df_curves.copy()
    df['phi'] = np.log(np.abs(df['discriminant']) + 1e-10) / \
        np.log(DELTA_MAX) * 360
    df['theta'] = np.log(np.abs(df['conductor']) + 1e-10) / \
        np.log(N_MAX) * 180
    df['z'] = PHI * df['rank']
    return df

# Align projections with cosmic data
def align_projections(df_cosmo, df_proj):
    df_cosmo_sample = df_cosmo.sample(
        n=len(df_proj), replace=True).reset_index(drop=True)
    df_proj = df_proj.reset_index(drop=True)
    aligned = []
    for cosmo_row, proj_row in zip(df_cosmo_sample.itertuples(index=False),
df_proj.itertuples(index=False)):
        row = dict(proj_row._asdict())
        row['ra'] = cosmo_row.ra
        row['dec'] = cosmo_row.dec
        row['comoving'] = cosmo_row.comoving_distance_mpc
        aligned.append(row)
    return pd.DataFrame(aligned)

# HD 3D Manifold Visualization with +/- axes and MP4 animation
def visualize_hd_manifold(df_proj, duration=45):
    scaler = StandardScaler()
    df_proj[['ra_norm', 'dec_norm', 'comoving_norm']
            ] = scaler.fit_transform(df_proj[['ra', 'dec', 'comoving']])
