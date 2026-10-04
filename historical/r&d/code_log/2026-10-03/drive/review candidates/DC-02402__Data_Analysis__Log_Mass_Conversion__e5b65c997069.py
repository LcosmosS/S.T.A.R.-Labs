sfr_bins = [-9999, -0.1, 0, 0.1, 1, 10]  # Example bins, adjust based on data
for i in range(len(sfr_bins) - 1):
    sfr_min = sfr_bins[i]
    sfr_max = sfr_bins[i+1]
    df_bin = df[(df['sfr'] >= sfr_min) & (df['sfr'] < sfr_max) & (df['sfr'] != -9999)]
    if not df_bin.empty:
        log_mass = df_bin['logmass'].values
        K = compute_K_theory(log_mass)
        skewness = pd.Series(log_mass).skew()
        mean_logmass = np.mean(log_mass)
        sd_logmass = np.std(log_mass, ddof=1)
        results.append({
            'sfr_range': f'{sfr_min} to {sfr_max}',
            'n_samples': len(df_bin),
            'K_theory': K,
            'skewness': skewness,
            'mean_logmass': mean_logmass,
            'sd_logmass': sd_logmass
        })


for result in results:
    print(f"sfr: {result['sfr_range']}, n={result['n_samples']}, K_theory={result['K_theory']:.4f}, "
          f"skewness={result['skewness']:.4f}, mean_logmass={result['mean_logmass']:.4f}, "
      *           f"sd_logmass={result['sd_logmass']:.4f}")
