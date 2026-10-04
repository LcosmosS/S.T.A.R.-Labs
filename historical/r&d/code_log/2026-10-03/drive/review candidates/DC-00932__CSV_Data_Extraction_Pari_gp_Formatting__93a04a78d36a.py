for group in range(5):
    group_indices = (groups == group)
    logmass_group = logmass[group_indices]
    k_theory = compute_K_theory(logmass_group)  # Replace with your function
    print(f"Group {group}: K_theory = {k_theory:.4f}, "
          f"Median z = {np.median(z[group_indices]):.4f}, "
                  3.           f"Median SFR = {np.median(sfr[group_indices]):.4f}")
