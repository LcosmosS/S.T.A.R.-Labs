    return summary


# --- 19. Shape Analysis --- 
def analyze_noise_points(df, feature_cols): 
    recursive_df = df[df['generator_type'] == 'Recursive'] 
    noise_df = recursive_df[recursive_df['structure_cluster'] == -1] 
    clustered_df = recursive_df[recursive_df['structure_cluster'] != -1] 
    noise_stats = noise_df[feature_cols].describe() 
    clustered_stats = clustered_df[feature_cols].describe() 
    noise_nan_prop = noise_df[feature_cols].isna().mean() 
    clustered_nan_prop = clustered_df[feature_cols].isna().mean() 
    noise_structure_dist = noise_df['generator_structure'].apply(lambda x: x['structure'] if isinstance(x, dict) else 'unknown').value_counts() 
    clustered_structure_dist = clustered_df['generator_structure'].apply(lambda x: x['structure'] if isinstance(x, dict) else 'unknown').value_counts() 
    selmer_status_dist = df['selmer_status'].value_counts() 
    stats_df = pd.concat([noise_stats, clustered_stats], axis=1, keys=['Noise', 'Clustered']) 
    stats_df.to_csv(f'{OUTPUT_PLOT_PREFIX}_noise_vs_clustered_stats.csv') 
    noise_nan_prop.to_csv(f'{OUTPUT_PLOT_PREFIX}_noise_nan_proportion.csv') 
    clustered_nan_prop.to_csv(f'{OUTPUT_PLOT_PREFIX}_clustered_nan_proportion.csv') 
    noise_structure_dist.to_csv(f'{OUTPUT_PLOT_PREFIX}_noise_structure_distribution.csv') 
    clustered_structure_dist.to_csv(f'{OUTPUT_PLOT_PREFIX}_clustered_structure_distribution.csv') 
    selmer_status_dist.to_csv(f'{OUTPUT_PLOT_PREFIX}_selmer_status_distribution.csv') 
    summary = {
        'Noise Points': len(noise_df),
        'Clustered Points': len(clustered_df)
    }
    analysis_logger.info("Noise Points Statistics:\n" + str(noise_stats))
    analysis_logger.info("\nClustered Points Statistics:\n" + str(clustered_stats))
    analysis_logger.info("\nNoise Points NaN Proportion:\n" + str(noise_nan_prop))
    analysis_logger.info("\nClustered Points NaN Proportion:\n" + str(clustered_nan_prop))
    analysis_logger.info("\nNoise Points Structure Distribution:\n" + str(noise_structure_dist))
    analysis_logger.info("\nClustered Points Structure Distribution:\n" + str(clustered_structure_dist))
    analysis_logger.info("\nSelmer Status Distribution:\n" + str(selmer_status_dist))
    return summary


# --- 20. Chunk Processing Function --- 
def process_chunk(chunk, chunk_idx, total_chunks):
    print_step(20, f"process_chunk (Chunk {chunk_idx+1}/{total_chunks})")
    pari = cypari2.Pari()
    chunk = impute_input_features(chunk)
    chunk['ra'] = chunk['ra'].where(chunk['ra'].notna(), -1)
    chunk['dec'] = chunk['dec'].where(chunk['dec'].notna(), -1)
    chunk['distance_mpc'] = chunk['z'].apply(calculate_distance_mpc)
    chunk['stellar_mass'] = chunk['logmass'].apply(convert_logmass_to_sm)
    chunk['radius_ly'] = chunk.apply(lambda x: estimate_radius_ly(x['petrorad_r'], x['distance_mpc']), axis=1)
    chunk[['reg_cosmo', 't_cosmo', 'log_delta', 'log_omega', 'log_torsion',
           'log_conductor', 'real_log_j', 'imag_log_j', 'tr_p1', 'var_ap',
           'sato_tate', 'isogeny_count', 'log_min_isogeny', 'log_torsion_type',
           'selmer_rank', 'selmer_status', 'torsion', 'j_invariant', 'discriminant', 'entropy', 'betti_1', 'entropy_gradient']] = chunk.apply(
               lambda x: compute_mappings(x, pari), axis=1)
    chunk[['generator_type', 'is_simple_generator']] = chunk.apply(classify_generator, axis=1, result_type='expand')
