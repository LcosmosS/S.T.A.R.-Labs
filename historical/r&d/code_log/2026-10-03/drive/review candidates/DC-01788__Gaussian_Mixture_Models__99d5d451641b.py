# Compute K for each subpopulation
for i in range(optimal_n):
    sub_df = df[df['subpopulation'] == i]
    masses = sub_df['mass'].values
    M0 = np.median(masses)
    sum_M_over_M0 = np.sum(masses / M0)
    sum_M0_over_M = np.sum(M0 / masses)
    K = sum_M_over_M0 / sum_M0_over_M
    print(f"Subpopulation {i}: K = {K:.4f}")
