        plt.figure(figsize=(8, 6))
        plt.hist(df[col].dropna(), bins=50, range=(df[col].quantile(0.01), df[col].quantile(0.99)),
                 density=True, alpha=0.7)
        plt.xlabel(col)
        plt.ylabel("Density")
        plt.title(f"Distribution of {col}")
        plt.savefig(f"dist_{col}.png", dpi=150)
        plt.close()
    else:
        print(f"{col}: Missing from dataset")

# Define s_range and plot L_cosmo_s vs log_SFR_Ha_raw
========================================================================
============================================================
s_vals = [0.5, 1.0, 1.5, 2.0]
for s in s_vals:
    col_name = f'L_cosmo_s_{s:.1f}'
    if col_name in df.columns:
        mask = df[col_name].notna() & df['log_SFR_Ha_raw'].notna() & np.isfinite(df[col_name]) &
np.isfinite(df['log_SFR_Ha_raw'])
        if mask.sum() < 10:
            print(f"Warning: Insufficient valid data for {col_name} plotting/fitting ({mask.sum()} valid
