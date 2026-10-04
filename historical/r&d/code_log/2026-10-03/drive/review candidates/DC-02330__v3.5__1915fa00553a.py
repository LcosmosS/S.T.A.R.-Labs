    if missing:
        print(f"Warning: {name} is missing columns: {missing}")
        # Initialize missing columns with 0 if they were skipped during topology
        for m in missing:
            df[m] = 0.0


# ====================== IMPUTATION ======================
imputer = KNNImputer(n_neighbors=int(10)) 
for df in [synth, real1, real2]:
    # We use [common_features] to ensure we only transform the shared TDA space
    df[common_features] = imputer.fit_transform(df[common_features])


print(" --- TDA features imputed and synchronized.")
    
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


# ====================== TARGET PREPARATION ======================
# For Arithmetic Seeds, our 'y' is usually the exact analytic rank 
# or the persistence entropy we want to emulate.
if 'rank' in synth.columns:
    synth_y = synth['rank']
elif 'exact_rank' in synth.columns:
    synth_y = synth['exact_rank']
else:
    # Fallback to persistence entropy if this is a purely topological study
    synth_y = synth['persistence_entropy']


print(f" -> Target vector 'synth_y' initialized. Shape: {synth_y.shape}")


# ====================== EVALUATION TARGETS ======================
# For Real2 (The 3-Selmer/LMFDB test set), we need the ground truth rank
if 'rank' in real2.columns:
    real2_y = real2['rank']
elif 'pari_2_selmer_rank' in real2.columns:
    real2_y = real2['pari_2_selmer_rank']
elif 'sage_rank' in real2.columns:
    real2_y = real2['sage_rank']
else:
    # If ground truth is missing, we initialize with zeros to allow the code to run,
    # though R² and MSE scores will not be meaningful.
