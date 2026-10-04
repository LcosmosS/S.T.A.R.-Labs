def compute_L_cosmo(logmass_vec, s):
    M = 10 ** logmass_vec
    M_sorted = np.sort(M)
    n = len(M)
    if n % 2 == 1:
        M0 = M_sorted[n // 2]
    else:
        M0 = (M_sorted[n // 2 - 1] + M_sorted[n // 2]) / 2
   *     return np.sum((M0 / M) ** s)
