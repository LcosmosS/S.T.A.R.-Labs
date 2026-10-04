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
        target_idx = subset['predicted_entropy'].idxmax() if s == 2 else
