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
