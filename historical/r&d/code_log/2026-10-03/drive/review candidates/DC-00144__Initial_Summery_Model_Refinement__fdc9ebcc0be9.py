df['cosmo_rank'] = gz_df['cosmo_rank']


# Step 2: L_cosmo(s) Construction
alpha = -1.5  # Adjusted alpha
M_star = df['log_Mass_gas'].median()
df['a_n'] = (10 ** df['log_Mass_gas'])**(1 + alpha) * np.exp(-10 ** df['log_Mass_gas'] / (10 ** M_star))
bins = pd.cut(df['Re_kpc'], bins=20, labels=False) + 1  # Bin by Re_kpc
df['z_bin'] = bins


# Check bin distribution
print("Bin distribution for Re_kpc:")
print(df['z_bin'].value_counts().sort_index())


# Plot L_cosmo(s) vs s
s_range = np.linspace(0.5, 2, 50)
# Compute grouped means and reindex to ensure all bins 1-20 are present
grouped_means = df.groupby('z_bin')['a_n'].mean().reindex(range(1, 21), fill_value=0)
L_vals = [grouped_means / (np.arange(1, 21) ** s) for s in s_range]
