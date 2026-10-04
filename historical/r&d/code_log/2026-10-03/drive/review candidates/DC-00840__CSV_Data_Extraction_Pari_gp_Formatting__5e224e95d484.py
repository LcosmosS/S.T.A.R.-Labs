for i in range(3):  # If you used 3 groups
    group_logmass = logmass[groups == i]
    group_z = np.array(z)[groups == i]
    group_sfr = np.array(sfr)[groups == i]
    group_ra = np.array(ra)[groups == i]
    print(f"Group {i}: Avg z = {np.mean(group_z)}, Avg sfr = {np.mean(group_sfr)}, Avg ra = {np.mean(group_ra)}")
