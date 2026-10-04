#===== Plot histogram for each feature ==================================================================================================================================================
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


# Define s_range and plot L_cosmo_s vs log_SFR_Ha_raw ====================================================================================================================================
s_vals = [0.5, 1.0, 1.5, 2.0]
for s in s_vals:
    col_name = f'L_cosmo_s_{s:.1f}'
    if col_name in df.columns:
        mask = df[col_name].notna() & df['log_SFR_Ha_raw'].notna() & np.isfinite(df[col_name]) & np.isfinite(df['log_SFR_Ha_raw'])
        if mask.sum() < 10:
            print(f"Warning: Insufficient valid data for {col_name} plotting/fitting ({mask.sum()} valid rows).")
            continue


# ===== Scatter plot =====================================================================================================================================================================
        plt.figure(figsize=(8, 6))
        plt.scatter(df.loc[mask, col_name], df.loc[mask, 'log_SFR_Ha_raw'], alpha=0.5, s=10)
        plt.xlabel(f"{col_name}")
        plt.ylabel("log_SFR_Ha_raw")
        plt.title(f"{col_name} vs log_SFR_Ha_raw")
        plt.savefig(f"L_cosmo_s{s:.1f}_vs_SFR.png", dpi=150)
        plt.close()


# ==== Polynomial fit plot ===============================================================================================================================================================
        try:
            poly_coeffs = Polynomial.fit(df.loc[mask, col_name], df.loc[mask, 'log_SFR_Ha_raw'], deg=2)
            x_fit = np.linspace(df.loc[mask, col_name].min(), df.loc[mask, col_name].max(), 100)
            y_fit = poly_coeffs(x_fit)
            y_pred = poly_coeffs(df.loc[mask, col_name])
            r2 = r2_score(df.loc[mask, 'log_SFR_Ha_raw'], y_pred)
            plt.figure(figsize=(8, 6))
            plt.scatter(df.loc[mask, col_name], df.loc[mask, 'log_SFR_Ha_raw'], alpha=0.5, s=10)
            plt.plot(x_fit, y_fit, 'r-', label=f'Quadratic Fit (R²={r2:.3f})')
            plt.xlabel(f"{col_name}")
            plt.ylabel("log_SFR_Ha_raw")
            plt.title(f"{col_name} vs log_SFR_Ha_raw with Polynomial Fit")
            plt.legend()
            plt.savefig(f"L_cosmo_s{s:.1f}_vs_SFR_fit.png", dpi=150)
            plt.close()
        except Exception as e:
            print(f"Warning: Polynomial fit failed for {col_name}: {e}")
    else:
        print(f"Warning: {col_name} not available for plotting.")


# Define features and target =============================================================================================================================================================
target = "log_SFR_Ha_raw"
features = [
    "logMass", "Re_kpc", "OH_O3N2_raw", "cosmo_rank",
    "mass_metallicity", "sqrt_Re_kpc", "cosmo_rank_mass", "L_cosmo_s1_mass",
    "log_flux_Ha", "log_flux_Hb", "log_flux_OIII_5007", "log_flux_NII_6584", 
    "log_e_flux_Ha", "L_cosmo_s_0.5", "L_cosmo_s_1.0", "L_cosmo_s_1.5", 
    "L_cosmo_s_2.0", "cluster_density"
]
if 'umag' in df.columns:
    features.extend(["color_ug", "color_gr", "color_ri", "color_iz", "e_color_ug", "e_color_gr"])
if 'Jmag' in df.columns:
    features.extend(["color_JK", "e_color_JK"])
if 'color_ug' in df.columns:
    features.extend(["color_ug", "color_gr", "color_ri", "color_iz", "e_color_ug", "e_color_gr"])
if 'color_JK' in df.columns:
    features.extend(["color_JK", "e_color_JK"])


# Global imputation before feature selection =============================================================================================================================================
numeric_cols = df.select_dtypes(include=[np.number]).columns
df[numeric_cols] = df[numeric_cols].replace([np.inf, -np.inf], np.nan).fillna(df[numeric_cols].median(skipna=True))


# Select features and target =============================================================================================================================================================
X = df[features]
y = df[target]
print(f"Rows after feature selection: {len(X)}")
print(f"NaN in y ({target}): {y.isna().sum()}")
