# Step 2: L_cosmo(s) Construction
alpha = -1.5
M_star = df['log_Mass_gas'].median()
df['a_n'] = (10 ** df['log_Mass_gas'])**(1 + alpha) * np.exp(-10 ** df['log_Mass_gas'] / (10 ** M_star))
bins = pd.cut(df['Re_kpc'], bins=20, labels=False) + 1
df['z_bin'] = bins


# Check bin distribution
print("Bin distribution for Re_kpc:")
print(df['z_bin'].value_counts().sort_index())


# Compute L_cosmo(s) with consistent column naming
s_vals = [0.5, 1.0, 1.5, 2.0]
for s in s_vals:
    # Use .format to ensure consistent string formatting
    col_name = 'L_cosmo_s{:.1f}'.format(s)
    df[col_name] = df.groupby('z_bin')['a_n'].transform('mean') / (df['z_bin'] ** s)


# Debug: Check column names
print("Columns after L_cosmo_s creation:", [col for col in df.columns if 'L_cosmo_s' in col])


df['cosmo_rank_L'] = df['cosmo_rank'] * df['L_cosmo_s1.0']


# Plot L_cosmo(s) vs s
s_range = np.linspace(0.5, 2, 50)
grouped_means = df.groupby('z_bin')['a_n'].mean().reindex(range(1, 21), fill_value=0)
L_vals = [grouped_means / (np.arange(1, 21) ** s) for s in s_range]
