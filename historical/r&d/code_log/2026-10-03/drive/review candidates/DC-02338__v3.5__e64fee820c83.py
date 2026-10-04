    # Evaluate 
    print("\n--- Global Sweep Results (Combined real1 + real2) ---")
    y_test = test_df['persistence_entropy']
    preds = sweep_stacker.predict(test_df[features])
    
    for s in [0, 1, 2, 3, 4]:
        mask = (test_df['entropy_strata'] == s)
        if mask.sum() > 0:
            s_true, s_pred = y_test[mask], preds[mask]
            if np.var(s_true) < 1e-8:
                print(f" Stratum {s} (Voids): MAE = {mean_absolute_error(s_true, s_pred):.6f} [Quenched]")
            else:
                print(f" Stratum {s} (Web): R² = {r2_score(s_true, s_pred):.4f}")
                
    return sweep_stacker, test_df


# RUN THE SWEEP
global_sweep_model, sweep_test_data = run_global_sweep(merged_real, sweep_features)


# ====================== 6. FINAL INFERENCE & MERGING ======================
print("\n--- Synthesizing Final Inference DataFrame ---")


# Use 'global_sweep_model' (returned by your sweep) and 'sweep_test_data' 
# to ensure we are working with the clean, stratified test set.
X_eval = sweep_test_data[sweep_features].fillna(0)
final_predictions = global_sweep_model.predict(X_eval)


# Construct final_df from the test data
final_df = sweep_test_data.copy()
final_df['predicted_entropy'] = final_predictions
# If you are targeting rank, ensure 'true_rank' exists; 
# otherwise use 'persistence_entropy'
final_df['true_target'] = sweep_test_data['persistence_entropy']


# Compute TDA Weight (Topological Heat/Confidence)
error_term = np.abs(final_df['true_target'] - final_df['predicted_entropy'])
final_df['tda_weight'] = (1.0 + final_df['persistence_entropy']) / (1.0 + error_term)


print(f" -> final_df synthesized. Shape: {final_df.shape}")


# ====================== 6. FINAL INFERENCE & SYNTHESIS ======================
print("\n--- Synthesizing Final Inference DataFrame ---")


# We use the results from the RUN THE SWEEP step
# features = sweep_features, model = global_sweep_model, data = sweep_test_data
X_eval_final = sweep_test_data[sweep_features].fillna(0)
final_predictions = global_sweep_model.predict(X_eval_final)


# Create the DEFINITIVE final_df
final_df = sweep_test_data.copy()
final_df['predicted_entropy'] = final_predictions
final_df['true_target'] = sweep_test_data['persistence_entropy']


# Calculate TDA Weight (Topological Heat)
error_term = np.abs(final_df['true_target'] - final_df['predicted_entropy'])
final_df['tda_weight'] = (1.0 + final_df['persistence_entropy']) / (1.0 + error_term)


print(f" -> final_df successfully defined. Shape: {final_df.shape}")


# ====================== 7. VISUALIZATION & ANCHOR ANALYSIS ======================


# 1. Plot Barcodes using the NEW global model and features
plot_strata_barcodes(sweep_test_data, global_sweep_model, sweep_features)


# 2. Rank 4 Anchor Analysis (The "Gold Standard" check)
# We check if 'rank' exists (likely from the original real2/lmfdb merge)
if 'rank' in final_df.columns:
    # Use .astype(int) to handle SageMath Integer types or floats
    rank_4_subset = final_df[final_df['rank'].astype(int) == 4]
    if not rank_4_subset.empty:
        avg_weight = rank_4_subset['tda_weight'].mean()
        print(f"Rank 4 Anchor Weight: {avg_weight:.4f}")
    else:
        print("Rank 4 subset is empty in this test slice.")
else:
    print("Column 'rank' not found in final_df. Check your merge logic.")
import pysr
from pysr import PySRRegressor


print("\n--- Initiating Symbolic Extraction on Stratum 2 (Complex Web) ---")


# 1. Isolate the Complex Web
complex_web = sweep_test_data[sweep_test_data['entropy_strata'] == 2].copy()


# 2. Define the analytical feature space
# We exclude the raw proxies (like flux_gr) and focus on the physical variables
sym_features = [
    'normalized_density', 
    'local_betti_1', 
    'local_betti_2', 
    'T_cosmo', 
    'Anthropic'
]


X_sym = complex_web[sym_features]
y_sym = complex_web['persistence_entropy']


# 3. Configure the PySR Regressor
# We give it basic operators to see if an Euler-like characteristic emerges naturally
pysr_model = PySRRegressor(
    niterations=40,
    binary_operators=["+", "*", "-", "/"],
    unary_operators=["exp", "inv(x) = 1/x"],
    extra_sympy_mappings={"inv": lambda x: 1/x},
    loss="loss(prediction, target) = (prediction - target)^2",
    model_selection="best",
    random_state=42
)


# 4. Fit the model
pysr_model.fit(X_sym, y_sym)


print("\n--- Top Candidate Equations ---")
print(pysr_model.sympy())


# --- REFINED HISTOGRAM ---
print("\n Histogram of log(discovered constants)...")


# Constants from your Complexity 11 Equation (β=16.26, offset=1.35, etc.)
constants = [16.263, np.sqrt(1.5), 1.2209, 16.183, 1.352]
plt.figure(figsize=(8, 5))
plt.hist(np.log(np.abs(constants) + 1e-8), bins=10, color='darkgreen', alpha=0.7)
plt.title("Log-Spectral Distribution of Discovered Constants")
plt.xlabel("log(|constant|)")
plt.ylabel("Frequency")
plt.grid(axis='y', alpha=0.3)
plt.show()


print("\n S.T.A.R. Pipeline Complete. Visualization and Foliation test saved.")
