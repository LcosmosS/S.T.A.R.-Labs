    print(f"File not found: {file_path}")
    exit(1)


# ... (rest of the data processing, filtering, GMM fitting, etc.)


# Compute K_values
grouped = df.groupby('subpopulation')
K_values = {}
for subpop, group in grouped:
    masses = group['mass'].values
    M0 = np.median(masses)
    sum_M_over_M0 = np.sum(masses / M0)
    sum_M0_over_M = np.sum(M0 / masses)
    K = sum_M_over_M0 / sum_M0_over_M
    K_values[subpop] = K
    print(f"Subpopulation {subpop}: M0 = {M0:.2e}, K = {K:.4f}")


# Compute rank
