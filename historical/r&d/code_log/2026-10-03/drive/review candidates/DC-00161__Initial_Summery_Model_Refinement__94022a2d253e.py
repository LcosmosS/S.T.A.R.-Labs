df['cosmo_rank'] = gz_df['cosmo_rank']


# Step 2: L_cosmo(s) Construction
alpha = -1.5
M_star = df['log_Mass_gas'].median()
df['a_n'] = (10 ** df['log_Mass_gas'])**(1 + alpha) * np.exp(-10 ** df['log_Mass_gas'] / (10 ** M_star))
# Use quantile-based binning
bins = pd.qcut(df['Re_kpc'], q=20, labels=False, duplicates='drop') + 1
df['z_bin'] = bins
n_bins = df['z_bin'].nunique()
print(f"Number of unique bins after qcut: {n_bins}")
print("Bin distribution for Re_kpc (after qcut):")
print(df['z_bin'].value_counts().sort_index())


# Compute L_cosmo(s) for multiple s values
s_vals = [0.5, 1.0, 1.5, 2.0]
s_range = np.linspace(0.5, 2, 50)
for s in s_vals:
    col_name = f'L_cosmo_s_{s:.1f}'
    df[col_name] = df.groupby('z_bin')['a_n'].transform('mean') / (df['z_bin'] ** s)


# Debug: Check columns
print("Columns after creating L_cosmo_s*:")
print(df.columns.tolist())


df['cosmo_rank_L'] = df['cosmo_rank'] * df['L_cosmo_s_1.0']


# Plot L_cosmo(s) vs s
grouped_means = df.groupby('z_bin')['a_n'].mean().reindex(range(1, n_bins + 1), fill_value=0)
L_vals = [grouped_means / (np.arange(1, n_bins + 1) ** s) for s in s_range]
