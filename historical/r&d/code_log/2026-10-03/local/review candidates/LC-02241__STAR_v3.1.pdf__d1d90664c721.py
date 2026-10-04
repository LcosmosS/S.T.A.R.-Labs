# --- FIT GLOBAL STACKER ---
# This fixes the NameError: 'stacker' is not defined
print("\n Fitting Final Global Stacker for multi-strata analysis...")
global_stacker = StableECCStacker(params=best_params)
global_stacker.fit(real2[common_features], real2_y, real2['entropy_strata'])

# --- MULTI-STRATA R² ANALYSIS ---
print("\n--- Robust Multi-Strata Analysis (Foliation Test) ---")
final_preds = global_stacker.predict(real2[common_features])

for s in [0, 1, 2]:
    mask = (real2['entropy_strata'] == s)
    if mask.sum() > 0: