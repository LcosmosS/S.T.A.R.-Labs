def compute_K_theory(logmass_vec):
M = 10 ** logmass_vec  # Convert logmass to stellar mass


M0 = np.median(M)      # Median mass


sum_M_over_M0 = np.sum(M / M0)


sum_M0_over_M = np.sum(M0 / M)


return sum_M_over_M0 / sum_M0_over_M
