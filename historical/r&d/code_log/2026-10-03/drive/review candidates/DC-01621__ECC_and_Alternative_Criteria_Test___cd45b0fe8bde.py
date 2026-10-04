# --- 10. Scientific Derivation Functions ---
def calculate_distance_mpc(z): 
    if z is None or not np.isfinite(z) or z <= 0: 
        return np.nan, {'Distance': np.nan, 'Status': 'Invalid input'}
    try: 
        distance = float(cosmo.comoving_distance(z).to(u.Mpc).value) 
        return distance, {'Distance': distance, 'Status': 'Computed'}
    except Exception as e: 
        logging.debug(f"calculate_distance_mpc: Error - {str(e)}")
        return np.nan, {'Distance': np.nan, 'Status': f'Error: {str(e)}'}


# --- 20. Chunk Processing Function ---
def process_chunk(chunk, chunk_idx, total_chunks):
    print_step(20, f"process_chunk (Chunk {chunk_idx+1}/{total_chunks})")
    pari = cypari2.Pari()
    chunk, impute_summary = impute_input_features(chunk)
    chunk['ra'] = chunk['ra'].where(chunk['ra'].notna(), -1)
    chunk['dec'] = chunk['dec'].where(chunk['dec'].notna(), -1)
    # Apply calculate_distance_mpc and unpack results
    distance_results = chunk['z'].apply(calculate_distance_mpc)
    chunk['distance_mpc'] = distance_results.apply(lambda x: x[0])
    distance_summaries = distance_results.apply(lambda x: x[1])
    chunk['stellar_mass'] = chunk['logmass'].apply(convert_logmass_to_sm)
    chunk['radius_ly'] = chunk.apply(lambda x: estimate_radius_ly(x['petrorad_r'], x['distance_mpc']), axis=1)
    chunk[['reg_cosmo', 't_cosmo', 'log_delta', 'log_omega', 'log_torsion',
           'log_conductor', 'real_log_j', 'imag_log_j', 'tr_p1', 'var_ap',
           'sato_tate', 'isogeny_count', 'log_min_isogeny', 'log_torsion_type',
           'selmer_rank', 'selmer_status', 'torsion', 'j_invariant', 'discriminant', 'entropy', 'betti_1', 'entropy_gradient']], mapping_summaries = chunk.apply(
               lambda x: compute_mappings(x, pari), axis=1, result_type='expand')
    chunk[['generator_type', 'is_simple_generator', 'generator_summary']] = chunk.apply(classify_generator, axis=1, result_type='expand')
