def L_k(s, masses, M_0):
    return np.sum((M_0 / masses) ** s)


# Compute L_k(s) at s=1 for each subpopulation
L_values = []
for i in range(optimal_n):
    subpopulation = df_filtered[df_filtered['subpopulation'] == i]
    masses = subpopulation['mass'].values
    M_0 = np.median(masses)
    L = L_k(1, masses, M_0)
    L_values.append(L)
