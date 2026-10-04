bin_indices = select(i -> z[i] >= 0.1332 && sfr[i] >= -0.0661, [1..n]);
logmass_bin = vector(#bin_indices, j, logmass[bin_indices[j]]);
K_combo = compute_K_theory(filter_IQR(logmass_bin));
* print("K_theory for z >= 0.1332 and sfr >= -0.0661: ", K_combo);
