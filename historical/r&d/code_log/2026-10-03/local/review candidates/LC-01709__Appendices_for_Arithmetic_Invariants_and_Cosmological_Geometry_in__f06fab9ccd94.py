    selmer_status_dist.to_csv(f'{OUTPUT_PLOT_PREFIX}_selmer_status_distribution.csv')

    print("Noise Points Statistics:\n", noise_stats)
    print("\nClustered Points Statistics:\n", clustered_stats)
    print("\nNoise Points NaN Proportion:\n", noise_nan_prop)
    print("\nClustered Points NaN Proportion:\n", clustered_nan_prop)
    print("\nNoise Points Structure Distribution:\n", noise_structure_dist)
    print("\nClustered Points Structure Distribution:\n", clustered_structure_dist)
    print("\nSelmer Status Distribution:\n", selmer_status_dist)

# --- 20. Main Processing ---