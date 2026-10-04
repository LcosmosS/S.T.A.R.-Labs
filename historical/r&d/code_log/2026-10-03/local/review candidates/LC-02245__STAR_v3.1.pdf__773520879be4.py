            else:
                print(f" Stratum {s} (Web): R² = {r2_score(s_true, s_pred):.4f}")

    return sweep_stacker, test_df

# RUN THE SWEEP
global_sweep_model, sweep_test_data = run_global_sweep(merged_real, sweep_features)

# UPDATE VISUALIZATION WITH GLOBAL MODEL
plot_strata_barcodes(sweep_test_data, global_sweep_model, sweep_features)

import pysr
from pysr import PySRRegressor

print("\n--- Initiating Symbolic Extraction on Stratum 2 (Complex Web) ---")

# 1. Isolate the Complex Web
complex_web = sweep_test_data[sweep_test_data['entropy_strata'] == 2].copy()

# 2. Define the analytical feature space