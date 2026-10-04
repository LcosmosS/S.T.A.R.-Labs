# --- 5. Main Unified Pipeline ---
def main():
    print("--- [STAGE 1/2] Starting THEORY-DRIVEN VALUATIVE Data Processing... ---")
    df_analysis = process_data()
    if df_analysis is None or df_analysis.empty:
        print("Pipeline halted due to lack of valid data."); return
        
    print(f"\n--- [STAGE 2/2] Final Synthesis: Two-Tiered Analysis... ---")
    run_final_synthesis(df_analysis)


def process_data():
    processed_chunks = []
    for i, chunk in enumerate(pd.read_csv(INPUT_FILE, usecols=REQUIRED_COLUMNS, chunksize=CHUNKSIZE, on_bad_lines='skip', low_memory=True)):
        print(f"  - Processing chunk {i+1}...")
        chunk.replace(-9999, np.nan, inplace=True); chunk.dropna(subset=REQUIRED_COLUMNS, inplace=True)
        chunk = chunk[chunk['z'] > 0].copy()
        if chunk.empty: continue


        chunk['distance_mpc'] = chunk['z'].apply(calculate_distance_mpc)
        chunk['mass_sm'] = chunk['logmass'].apply(convert_logmass_to_sm)
        chunk['radius_ly'] = chunk.apply(lambda row: estimate_radius_ly(row['petrorad_r'], row['distance_mpc']), axis=1)
        chunk['virial_energy_j'] = chunk.apply(lambda row: calculate_virial_energy(row['mass_sm'], row['radius_ly']), axis=1)
        
        distance_mly = chunk['distance_mpc'] * 3.26156
        chunk['density_kg_m3'] = chunk.apply(lambda row: (row['mass_sm'] * 1.989e30) / ((4/3) * np.pi * (row['radius_ly'] * 9.461e15)**3) if pd.notna(row['mass_sm']) and pd.notna(row['radius_ly']) and row['radius_ly'] > 0 else np.nan, axis=1)
        
        coeffs = chunk.apply(lambda row: map_physics_to_curve_coeffs(distance_mly.get(row.name), row['density_kg_m3']), axis=1)
        chunk[['coeff_a', 'coeff_b']] = pd.DataFrame(coeffs.tolist(), index=chunk.index)
        
        def process_curve_properties(row):
            if pd.isna(row['coeff_a']) or pd.isna(row['coeff_b']): return (np.nan, 'Invalid Curve', {})
            try:
                E = EllipticCurve(QQ, [0, 0, 0, row['coeff_a'], row['coeff_b']])
                discriminant = E.discriminant()
                return (discriminant, estimate_rank_category(E), get_prime_factor_exponents(discriminant))
            except: return (np.nan, 'Invalid Curve', {})
        
        results = chunk.apply(process_curve_properties, axis=1)
        chunk[['discriminant_sage', 'rank', 'prime_exponents']] = pd.DataFrame(results.tolist(), index=chunk.index)
        
        processed_chunks.append(chunk)
