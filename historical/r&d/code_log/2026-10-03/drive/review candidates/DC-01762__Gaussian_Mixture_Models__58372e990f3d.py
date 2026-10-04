print(f"Rank (number of subpopulations with K ≈ 1): {rank}")


# Step 4: Refine L-Function Definition
def L_k(s, masses, M_0):
    return np.sum((M_0 / masses) ** s)


L_values = []
for i in range(optimal_n):
    subpopulation = df_filtered[df_filtered['subpopulation'] == i]
    masses = subpopulation['mass'].values
    M_0 = np.median(masses)
    L = L_k(1, masses, M_0)
    L_values.append(L)
    print(f"Subpopulation {i}: L_k(1) = {L:.4f}")


L_cosmo = np.prod(L_values)
print(f"L_cosmo(1) = {L_cosmo:.4f}")
