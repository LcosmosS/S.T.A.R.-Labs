    mass_kg = mass_sm * 1.989e30; radius_m = radius_ly * 9.461e15
    potential_energy = -1 * G.value * (mass_kg ** 2) / radius_m
    return potential_energy / 2.0

# --- 4. SageMath Core Hypothesis Functions (unchanged) ---
def map_physics_to_curve_coeffs(distance_mly, density_kg_m3):
    if not (np.isfinite(distance_mly) and np.isfinite(density_kg_m3)): return np.nan,
np.nan
    return QQ(-distance_mly), QQ(density_kg_m3)

# --- 5. Main Unified Pipeline ---
def main():
    print("--- [STAGE 1/4] Starting HIGH-FIDELITY Data Processing... ---")
    df_analysis = process_data()
    if df_analysis is None or df_analysis.empty:
        print("Pipeline halted due to lack of valid data."); return

    print(f"\n--- [STAGE 2/4] Full-Population Exploratory Analysis... ---")
    df_clean = clean_and_prepare_data(df_analysis)
    run_exploratory_analysis(df_clean)

    print(f"\n--- [STAGE 3/4] Predictive Modeling with 75/25 Split... ---")
    run_predictive_modeling(df_clean)

    print(f"\nDefinitive predictive analysis complete. All plots saved with prefix
