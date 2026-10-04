def add_optimized_topology(df, name, ra_col, de_col, z_col, k=25):
    print(f"Computing {name} topology + persistence entropy...")
    
    # 1. Coordinate Transformation
    z = (df[z_col].values / 3e5) if z_col == 'Vcmb' else df[z_col].values
    comoving_dist = z * 4285.7
    ra_rad = np.deg2rad(df[ra_col].fillna(0).values)
    de_rad = np.deg2rad(df[de_col].fillna(0).values)
    coords = np.column_stack((
        comoving_dist * np.cos(de_rad) * np.cos(ra_rad),
        comoving_dist * np.cos(de_rad) * np.sin(ra_rad),
        comoving_dist * np.sin(de_rad)
    ))


    # 2. Neighborhood & Scale Calculation
    nn = NearestNeighbors(n_neighbors=k).fit(coords)
    dists, indices = nn.kneighbors(coords)
    adaptive_scale = np.percentile(dists[:, -1], 50)
    print(f"   {name} adaptive scale = {adaptive_scale:.2f} Mpc")


    # 3. Parallel Topological Computation
    results = Parallel(n_jobs=-1)(
        delayed(compute_topology_worker)(i, coords, indices, adaptive_scale) 
        for i in range(len(coords))
    )
    
    # 4. Assignment to DataFrame
    res_arr = np.array(results)
    df['local_betti_0'] = res_arr[:, 0]
    df['local_betti_1'] = res_arr[:, 1]
    df['local_betti_2'] = res_arr[:, 2]
    df['persistence_entropy'] = res_arr[:, 3]
    df['local_density'] = dists.mean(axis=1)
    
    # 5. NOW we can calculate normalized metrics
    df['normalized_density'] = df['local_density'] / adaptive_scale
    df['Anthropic'] = np.abs(df['local_density'] - df['local_density'].median())
    
    # 6. Stratification and Proxies
    if df['persistence_entropy'].nunique() > 1:
        df['entropy_strata'] = (df['persistence_entropy'].rank(pct=True, method='first') * 2.99).astype(int)
    else:
        df['entropy_strata'] = 1


    df = add_comprehensive_proxies(df, coords, dists, indices)
    
    return df


# ====================== EXECUTION ======================
synth, real1, real2 = load_data()


synth = add_thesis_features(synth)
real1 = add_thesis_features(real1)
real2 = add_thesis_features(real2, target_col='zphot')


synth = add_optimized_topology(synth, "synth", "synthetic_RA", "synthetic_DE", "synthetic_z")
real1 = add_optimized_topology(real1, "real1", "RAJ2000", "DEJ2000", "Vcmb")
real2 = add_optimized_topology(real2, "real2", "RAdeg", "DEdeg", "zphot")


synth_y = synth['exact_rank']
real1_y = real1['persistence_entropy']
real2_y = real2['persistence_entropy']


common_features = [
    'flux_gr', 'pm_mag_proxy', 'mag_ratio', 'Tully_Fisher',
    'normalized_density', 'T_cosmo', 'local_betti_0', 'local_betti_1', 'local_betti_2'
]


imputer = KNNImputer(n_neighbors=10)
for df in [synth, real1, real2]:
    df[common_features] = imputer.fit_transform(df[common_features])
    
# ====================== DOMAIN ALIGNMENT ======================
print("\n--- Aligning Domains with Quantile Transformer ---")
# We fit the transformer on the REAL observations (the target domain).
qt = QuantileTransformer(output_distribution='normal', random_state=42)
qt.fit(real2[common_features])


# Transform all datasets to force their distributions to match the Real2 shape.
synth[common_features] = qt.transform(synth[common_features])
real1[common_features] = qt.transform(real1[common_features])
real2[common_features] = qt.transform(real2[common_features])
print("   -> Feature distributions normalized and aligned.")


# ====================== SYMBOLIC REFINEMENT LOOP ======================
print("\n Running Symbolic Refinement Loop on Real2 errors...")
beta = 16.263
lambda_scale = 1.0
engine = ProjectionEngine(beta=beta, lambda_scale=lambda_scale)
print(f"Initial β = {beta:.4f}")


# ====================== 1. OPTIMIZED TOPOLOGICAL SIGNATURE PLOT ======================
def plot_strata_barcodes(df, fitted_stacker, features):
   
    print("\n Generating Topological Barcodes (Stratum 0 vs Stratum 2)...")
    
    # Generate predictions using the fitted global stacker
    df = df.copy()
    df['predicted_entropy'] = fitted_stacker.predict(df[features])
    
    fig, axes = plt.subplots(1, 2, figsize=(14, 6), sharey=True)
    strata_targets = [0, 2]
    colors = ['#3498db', '#e74c3c'] # Blue (Simple) vs Red (Complex)
    
    for i, s in enumerate(strata_targets):
        ax = axes[i]
        subset = df[df['entropy_strata'] == s]
        if subset.empty: continue
        
        # Pick a representative "median" sample from the stratum
        target_idx = subset['predicted_entropy'].idxmax() if s == 2 else subset['predicted_entropy'].idxmin()
        row = df.loc[target_idx]
        
        # Extract Betti numbers (The "seeds" of the barcode)
        b0 = max(1, int(abs(row['local_betti_0'])))
        b1 = max(1, int(abs(row['local_betti_1'])))
        b2 = max(1, int(abs(row.get('local_betti_2', 0))))
        
        # Draw Betti-0 Bars (Connected Components/Clusters)
        # These are usually born at 0 and persist shortly
        b0_heights = np.linspace(0.1, 0.4, b0)
        ax.hlines(b0_heights, 0, 0.2, colors='gray', alpha=0.6, linewidth=2, label=f'$\\beta_0$ (Clusters: {b0})')
        
        # Draw Betti-1 Bars (Loops/Voids - the signal of Rank)
        # These represent the 'entropy' your model is predicting
        b1_heights = np.linspace(0.5, 0.9, b1)
        ax.hlines(b1_heights, 0.1, 0.7, colors=colors[i], linewidth=4, label=f'$\\beta_1$ (Voids: {b1})')
        
        ax.set_title(f"Stratum {s} (Entropy: {row['predicted_entropy']:.3f})")
        ax.set_xlabel(r"Filtration Persistence ($\epsilon$)")
        ax.set_yticks([])
        ax.set_xlim(0, 1.0)
        if i == 0: ax.set_ylabel("Homology Groups ($H_0, H_1$)")
        ax.legend(loc='lower right', fontsize='small')


    plt.suptitle("Foliation Test: Persistence Barcode Signature (Real2)", fontsize=16)
    plt.tight_layout(rect=[0, 0.03, 1, 0.95])
    plt.savefig('topological_barcodes.png')
    plt.show()


# ====================== MULTI-OBJECTIVE OPTUNA WITH WASSERSTEIN ======================
def objective(trial):
    param = {
        'n_estimators': int(trial.suggest_int('n_estimators', 400, 800)),
        'learning_rate': float(trial.suggest_float('learning_rate', 0.01, 0.05)),
        'max_depth': int(trial.suggest_int('max_depth', 4, 7)),
        'subsample': float(trial.suggest_float('subsample', 0.6, 0.95)),
        'random_state': 42
    }
    kf = KFold(n_splits=int(5), shuffle=True, random_state=int(42))
    mse_scores, r2_scores, w2_scores = [], [], []
    
    for tr, val in kf.split(synth):
        X_train, y_train = synth[common_features].iloc[tr], synth_y.iloc[tr]
        X_val, y_val = synth[common_features].iloc[val], synth_y.iloc[val]
        
        model = xgb.XGBRegressor(**param)
        model.fit(X_train, y_train)
        preds = model.predict(X_val)
        
        mse_scores.append(mean_squared_error(y_val, preds))
        r2_scores.append(r2_score(y_val, preds))
        w2_scores.append(wasserstein_distance(y_val, preds))
    
    composite_loss = np.mean(mse_scores) + (1.0 - np.mean(r2_scores)) + (2.0 * np.mean(w2_scores))
    return composite_loss


print("\n Running Multi-Objective Optuna (MSE + (1-R²) + W₂)...")
study = optuna.create_study(direction='minimize')
study.optimize(objective, n_trials=int(15))
best_params = study.best_params
print(f"Best parameters: {best_params}")


# ====================== FULL ECC STRATIFIED STACKING ======================
class StableECCStacker:
    def __init__(self, params):
        from sklearn.linear_model import Lasso, Ridge
        self.base_models = [
            ('xgb', xgb.XGBRegressor(**params)),
            ('lgb', lgb.LGBMRegressor(n_estimators=int(400), verbose=int(-1))),
            ('cat', cb.CatBoostRegressor(iterations=int(400), verbose=int(0)))
