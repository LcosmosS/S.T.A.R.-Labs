def compute_K_theory(log_mass):
    M = 10 ** log_mass
    M_sorted = np.sort(M)
    n = len(M)
    if n % 2 == 0:
        M0 = (M_sorted[n//2 - 1] + M_sorted[n//2]) / 2
    else:
        M0 = M_sorted[n//2]
    sum_M_over_M0 = np.sum(M / M0)
    sum_M0_over_M = np.sum(M0 / M)
    K_theory = sum_M_over_M0 / sum_M0_over_M
         *     return K_theory
         * Compute skewness using pd.Series(log_mass).skew(), mean_logmass with np.mean(log_mass), and sd_logmass with np.std(log_mass, ddof=1) for each group.
         4. Analyze Results:
         * Compare K_{\text{theory}} and skewness across different z and sfr groups, looking for combinations where K_{\text{theory}} is closer to 1 and skewness is closer to 0, indicating better fit to log-normal assumptions. Compare with simulated data, where K_{\text{theory}} \approx 1.077 and skewness ≈ 0.0088, to assess data quality.
         * Identify trends, such as whether high_sfr galaxies at certain z ranges show better fits, potentially linking to star-forming galaxy properties, or if low_sfr galaxies (quiescent) deviate more, suggesting different mass distribution behaviors.
         5. Visualize Distributions (Optional):
         * Use Python’s matplotlib (Matplotlib) or seaborn for visualization, creating histograms of log_mass for different z and sfr groups to visually inspect distribution shapes. For example, plot plt.hist(log_mass, bins=30, density=True) for high_sfr vs. low_sfr within z: 0.05 to 0.1 to see if one is more symmetric.
         * Create scatter plots of log_mass vs. z, colored by sfr, to identify patterns or clusters where the distribution might be more log-normal, using plt.scatter(z, log_mass, c=sfr, cmap='viridis').
         6. Explore Correlations and Refinement:
         * Check correlations between sfr and K_theory or skewness within z bins, using pd.corr() to see if star formation rate influences deviations, potentially indicating theoretical adjustments needed.
         * If certain groups show better fits, consider applying additional filtering, like IQR on log_mass within those groups, to remove outliers and recompute, assessing if K_theory improves.
