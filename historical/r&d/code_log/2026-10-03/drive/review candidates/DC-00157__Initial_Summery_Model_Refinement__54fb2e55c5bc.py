# After creating L_cosmo_s* columns
for s in s_vals:
    df[f'L_cosmo_s{s}'] = df.groupby('z_bin')['a_n'].transform('mean') / (df['z_bin'] ** s)
print("Columns after creating L_cosmo_s*:")
print(df.columns.tolist())
