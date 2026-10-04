bins = pd.qcut(df['Re_kpc'], q=20, labels=False, duplicates='drop') + 1
df['z_bin'] = bins
n_bins = df['z_bin'].nunique()
print(f"Number of unique bins after qcut: {n_bins}")
print("Bin distribution for Re_kpc (after qcut):")
print(df['z_bin'].value_counts().sort_index())

s_vals = [0.5, 1.0, 1.5, 2.0]
s_range = np.linspace(0.5, 2, 50)
for s in s_vals:
    col_name = f'L_cosmo_s_{s:.1f}'
    df[col_name] = df.groupby('z_bin')['a_n'].transform('mean') / (df['z_bin'] ** s)

print("Columns after creating L_cosmo_s*:")
print(df.columns.tolist())

print("Checking for NaN/infinite values in cosmo_rank and L_cosmo_s_1.0:")
print("cosmo_rank NaN count:", df['cosmo_rank'].isna().sum())
print("L_cosmo_s_1.0 NaN count:", df['L_cosmo_s_1.0'].isna().sum())
print("cosmo_rank infinite count:", np.isinf(df['cosmo_rank']).sum())
print("L_cosmo_s_1.0 infinite count:", np.isinf(df['L_cosmo_s_1.0']).sum())

df['cosmo_rank_L'] = df['cosmo_rank'] * df['L_cosmo_s_1.0']
df['cosmo_rank_L'] = df['cosmo_rank_L'].replace([np.inf, -np.inf], np.nan).fillna(0)
print("cosmo_rank_L created, NaN count:", df['cosmo_rank_L'].isna().sum())
