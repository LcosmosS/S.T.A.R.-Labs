n = #logmass;
print("Total number of entries: ", n);


filtered_logmass = filter_IQR(logmass);
K_full = compute_K_theory(filtered_logmass);
print("K_theory for full dataset: ", K_full);
kurtosis_full = compute_kurtosis(logmass);
print("Kurtosis for full dataset (logmass): ", kurtosis_full);


compute_subgroup_K_theory("z");
compute_subgroup_K_theory("sfr");
compute_subgroup_K_theory("ra");
compute_subgroup_K_theory("petrorad_r");
compute_subgroup_K_theory("dec");
compute_subgroup_K_theory("ellipticity");
