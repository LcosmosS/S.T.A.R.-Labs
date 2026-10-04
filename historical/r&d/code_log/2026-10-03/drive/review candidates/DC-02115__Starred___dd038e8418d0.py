print("\nScript completed successfully!")
def compute_K_theory(logmass_vec): M = 10 ** logmass_vec # Convert logmass to mass M_sorted = np.sort(M) n = len(M) if n == 0: return 0 # Median mass if n % 2 == 1: M0 = M_sorted[n // 2] else: M0 = (M_sorted[n // 2 - 1] + M_sorted[n // 2]) / 2 sum_M_over_M0 = np.sum(M / M0) sum_M0_over_M = np.sum(M0 / M) return sum_M_over_M0 / sum_M0_over_M
