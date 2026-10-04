        y_true = real2_y[mask]
        y_pred = final_preds[mask]

        variance = np.var(y_true)
        mae = mean_absolute_error(y_true, y_pred)

        # Guard against the Zero-Variance Trap
        if variance < 1e-8:
            print(f"   Stratum {s} (Entropy {s}): Variance near zero. R² undefined.")
            print(f"      -> MAE = {mae:.6f} (Model successfully quenched)")
        else:
            r2 = r2_score(y_true, y_pred)
            print(f"   Stratum {s} (Entropy {s}): R² = {r2:.4f} | MAE = {mae:.4f}")

# --- VISUALIZATION ---
plot_strata_barcodes(real2, global_stacker, common_features)

# ====================== S.T.A.R. v3.5 GLOBAL SWEEP ======================

# 1. Merge real1 and real2 to maximize training signal
print("\n--- Merging Catalogs for Global Sweep ---")
# Ensure we only use columns present in both datasets
common_cols = list(set(real1.columns).intersection(set(real2.columns)))
merged_real = pd.concat([real1[common_cols], real2[common_cols]],
axis=0).reset_index(drop=True)

# 2. Refined Feature Set for Structural Geometry
# We remove raw photometric proxies to focus the model on the 'Shape'
sweep_features = [
    'betti_ratio', 'local_anisotropy', 'density_gradient', 'void_gap',
    'local_betti_0', 'local_betti_1', 'local_betti_2', 'T_cosmo'
]

def run_global_sweep(df, features):
    print(f"Initiating Global Sweep on {len(df)} total galaxies...")
    from sklearn.model_selection import train_test_split

    # Clean any merge artifacts
    df = df.dropna(subset=['persistence_entropy', 'entropy_strata'])
    df[features] = df[features].fillna(0)

    # Stratified Split (80/20)
    train_df, test_df = train_test_split(
        df, test_size=float(0.2), stratify=df['entropy_strata'], random_state=42