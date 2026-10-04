def compute_K_theory(logmass):
    M = 10 ** logmass  # Convert to stellar mass
    M0 = np.median(M)  # Median mass
    sum1 = np.sum(M / M0)
    sum2 = np.sum(M0 / M)
    return sum1 / sum2


            * k_theory = compute_K_theory(logmass_group2)
