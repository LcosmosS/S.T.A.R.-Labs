def compute_L_cosmo(logmass_vec, s):
    M = 10 ** logmass_vec
    M_sorted = np.sort(M)
    n = len(M)
    if n % 2 == 1:
        M0 = M_sorted[n // 2]
    else:
        M0 = (M_sorted[n // 2 - 1] + M_sorted[n // 2]) / 2
    return np.sum((M0 / M) ** s)


# Compute L_cosmo at s=1 for each group
for i in range(gmm.n_components):
    group_logmass = logmass[groups == i]
    L_cosmo = compute_L_cosmo(group_logmass, 1)
    print(f"Group {i}: L_cosmo(s=1) = {L_cosmo:.4f}")
