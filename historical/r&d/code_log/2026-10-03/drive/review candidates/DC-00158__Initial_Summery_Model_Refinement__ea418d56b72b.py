# Step 2: L_cosmo(s) Construction
alpha = -1.5
M_star = df['log_Mass_gas'].median()
df['a_n'] = (10 ** df['log_Mass_gas'])**(1 + alpha) * np.exp(-10 ** df['log_Mass_gas'] / (10 ** M_star))
bins = pd.cut(df['Re_kpc'], bins=20, labels=False) + 1
df['z_bin'] = bins


# Check bin distribution
print("Bin distribution for Re_kpc:")
print(df['z_bin'].value_counts().sort_index())


# Compute L_cosmo(s) for multiple s values
s_vals = [0.5, 1.0, 1.5, 2.0]
for s in s_vals:
    col_name = f'L_cosmo_s_{s:.1f}'  # e.g., L_cosmo_s_0.5, L_cosmo_s_1.0
    df[col_name] = df.groupby('z_bin')['a_n'].transform('mean') / (df['z_bin'] ** s)


# Debug: Check columns
print("Columns after creating L_cosmo_s*:")
print(df.columns.tolist())


df['cosmo_rank_L'] = df['cosmo_rank'] * df['L_cosmo_s_1.0']
