# --- FIT GLOBAL STACKER ---
# This fixes the NameError: 'stacker' is not defined
print("\n Fitting Final Global Stacker for multi-strata analysis...")
global_stacker = StableECCStacker(params=best_params)
global_stacker.fit(real2[common_features], real2_y, real2['entropy_strata'])


# --- MULTI-STRATA R² ANALYSIS ---
print("\n--- Robust Multi-Strata Analysis (Foliation Test) ---")
final_preds = global_stacker.predict(real2[common_features]) 


for s in [0, 1, 2, 3, 4]:
    mask = (real2['entropy_strata'] == s)
    if mask.sum() > 0:
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


rank_4_subset = final_df[final_df['rank'] == 4]
if not rank_4_subset.empty:
    print(f"Rank 4 Anchor Weight: {rank_4_subset['tda_weight'].mean():.4f}")
    print(f"Average Rank 0-1 Weight: {final_df[final_df['rank'] <= 1]['tda_weight'].mean():.4f}")
    
# ====================== S.T.A.R. v3.5 GLOBAL SWEEP ======================


# 1. Merge real1 and real2 to maximize training signal
print("\n--- Merging Catalogs for Global Sweep ---")
# Ensure we only use columns present in both datasets
common_cols = list(set(real1.columns).intersection(set(real2.columns)))
merged_real = pd.concat([real1[common_cols], real2[common_cols]], axis=0).reset_index(drop=True)


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
    )
    
    # Initialize Stacker with your optimized best_params
    sweep_stacker = StableECCStacker(best_params)
    
    # Train on the combined weight of both catalogs
    sweep_stacker.fit(
        train_df[features], 
        train_df['persistence_entropy'], 
