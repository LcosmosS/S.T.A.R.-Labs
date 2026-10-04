        persistence = simplex_tree.persistence()
        # Find the feature with maximum persistence (Death - Birth)
        max_p = 0
        anchor_feature = None
        
        for dim, (b, d) in persistence:
            if d != float('inf'):
                lifetime = d - b
                if lifetime > max_p:
                    max_p = lifetime
                    anchor_feature = (dim, b, d)
        
        return {"max_lifetime": max_p, "feature": anchor_feature}
    
# 2. EXPLICIT INSTANTIATION (Fixes NameError)
print("\n--- Initializing Global Stacker with Robust Meta-Models ---")
global_stacker = StableECCStacker(best_params)


# Define evaluation data
X_eval = real2[common_features].fillna(0)
y_eval = real2_y
strata_eval = real2['entropy_strata']


# Fit and Predict
global_stacker.fit(X_eval, y_eval, strata_eval)
final_preds = global_stacker.predict(X_eval)


# 3. FOLIATION TEST
print("\n--- Fixed Multi-Strata R² Analysis ---")
for s in [0, 1, 2, 3, 4]:
    mask = (strata_eval == s)
    if mask.sum() > 0:
        r2 = r2_score(y_eval[mask], final_preds[mask])
        print(f"   Stratum {s} R² = {r2:.4f}")


# 4. CALL VISUALIZATION
plot_strata_barcodes(real2, global_stacker, common_features)


# --- FIT GLOBAL STACKER ---
