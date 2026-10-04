    df_analysis = pd.concat(processed_chunks, ignore_index=True)
    print(f"  - Data processing complete. {len(df_analysis)} high-fidelity rows finalized.")
    return df_analysis


def run_final_synthesis(df):
    # --- TIER 1: VALUATIVE PREDICTION (Full Dataset) ---
    print("\n  --- Part 1: Valuative Prediction on Full High-Fidelity Dataset ---")
    df_full = df.dropna(subset=['virial_energy_j', 'prime_exponents']).copy()
    df_full = df_full[(df_full['virial_energy_j'] != 0) & (df_full['prime_exponents'].str.len() > 0)]
    
    if df_full.empty:
        print("    - No valid data available for valuative prediction. Skipping.")
    else:
        print(f"    - Using all {len(df_full)} valid rows for valuative prediction.")
        df_full['log_abs_virial_energy'] = np.log10(np.abs(df_full['virial_energy_j']))
        df_exponents = pd.json_normalize(df_full['prime_exponents']).fillna(0)
        
        for p in TARGET_PRIMES:
            if p not in df_exponents.columns: df_exponents[p] = 0
        
        feature_cols = [p for p in TARGET_PRIMES if p in df_exponents.columns]
        X, y = df_exponents[feature_cols], df_full['log_abs_virial_energy']


        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=42)
        pipeline = Pipeline([('scaler', StandardScaler()), ('model', lgb.LGBMRegressor(random_state=42))])
        pipeline.fit(X_train, y_train)
        r2 = r2_score(y_test, pipeline.predict(X_test))
        
        print("\n" + "="*80); print("      VALUATIVE NORMALIZATION: PREDICTING ENERGY FROM ARITHMETIC STRUCTURE"); print("="*80)
        print(f"  - Predictive Model Fit (R² Score): {r2:.6f}"); print("="*80)


        feature_importances = pipeline.named_steps['model'].feature_importances_
        importance_df = pd.DataFrame({'feature': X_train.columns.astype(str), 'importance': feature_importances}).sort_values('importance', ascending=False).head(15)
        plt.figure(figsize=(12, 8)); sns.barplot(x='importance', y='feature', data=importance_df, palette='viridis', orient='h')
        plt.title("Valuative Prediction: Importance of Prime Factors in Predicting Energy", fontsize=16)
        plt.xlabel("Feature Importance", fontsize=12); plt.ylabel("Prime Factor of the Discriminant", fontsize=12)
        plt.savefig(f"{OUTPUT_PLOT_PREFIX}_valuative_feature_importance.png"); plt.close()
        print("    - Valuative feature importance plot saved.")


    # --- TIER 2: HIERARCHICAL VALIDATION (Tractable Subset) ---
    print("\n  --- Part 2: Hierarchical Validation on Computationally Tractable Subset ---")
    tractable_ranks = ['Rank 0', 'Rank 1', 'Rank 2', 'Rank 3+']
    df_ranked = df_full[df_full['rank'].isin(tractable_ranks)].copy()
    
    if df_ranked.empty:
        print("    - SCIENTIFIC FINDING: No galaxies with a computationally tractable rank were found in this dataset.")
        print("    - This validates the 'Zone of Intractability' hypothesis. No hierarchical plots will be generated.")
    else:
        print(f"    - Found {len(df_ranked)} galaxies with a computationally tractable rank for hierarchical analysis.")
        plt.figure(figsize=(12, 8))
        sns.violinplot(x='rank', y='log_abs_virial_energy', data=df_ranked, order=tractable_ranks, palette='plasma')
        plt.title("Hierarchical Validation: Virial Energy Distribution by Predicted Rank", fontsize=16)
        plt.xlabel("Predicted Algebraic Rank Category", fontsize=12)
        plt.ylabel("log10(|Virial Energy|)", fontsize=12)
        plt.savefig(f"{OUTPUT_PLOT_PREFIX}_hierarchical_rank_distribution.png"); plt.close()
        print("    - Hierarchical validation plot saved.")


if __name__ == "__main__":
    main()
