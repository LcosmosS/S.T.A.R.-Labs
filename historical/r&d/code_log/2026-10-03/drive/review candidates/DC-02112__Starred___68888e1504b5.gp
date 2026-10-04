n = #logmass;
print("Total number of entries: ", n);


# Full dataset
filtered_logmass = filter_IQR(logmass);
K_full = compute_K_theory(filtered_logmass);
kurtosis_full = compute_kurtosis(filtered_logmass);
print("K_theory for full dataset: ", K_full);
print("Kurtosis for full dataset: ", kurtosis_full);


# For z
sorted_z = vecsort(z);
z1 = sorted_z[floor(n/3)];
z2 = sorted_z[floor(2*n/3)];
print("z tertiles: ", z1, " and ", z2);
bin1_indices = select(i -> z[i] < z1, [1..n]);
logmass_bin1 = vector(#bin1_indices, j, logmass[bin1_indices[j]]);
filtered_bin1 = filter_IQR(logmass_bin1);
K_bin1 = compute_K_theory(filtered_bin1);
kurtosis_bin1 = compute_kurtosis(logmass_bin1);
print("K_theory for z < ", z1, ": ", K_bin1);
print("Kurtosis for z < ", z1, ": ", kurtosis_bin1);
bin2_indices = select(i -> z[i] >= z1 && z[i] < z2, [1..n]);
logmass_bin2 = vector(#bin2_indices, j, logmass[bin2_indices[j]]);
filtered_bin2 = filter_IQR(logmass_bin2);
K_bin2 = compute_K_theory(filtered_bin2);
kurtosis_bin2 = compute_kurtosis(logmass_bin2);
print("K_theory for ", z1, " <= z < ", z2, ": ", K_bin2);
print("Kurtosis for ", z1, " <= z < ", z2, ": ", kurtosis_bin2);
bin3_indices = select(i -> z[i] >= z2, [1..n]);
logmass_bin3 = vector(#bin3_indices, j, logmass[bin3_indices[j]]);
filtered_bin3 = filter_IQR(logmass_bin3);
K_bin3 = compute_K_theory(filtered_bin3);
kurtosis_bin3 = compute_kurtosis(logmass_bin3);
print("K_theory for z >= ", z2, ": ", K_bin3);
print("Kurtosis for z >= ", z2, ": ", kurtosis_bin3);


# For sfr
sorted_sfr = vecsort(sfr);
sfr1 = sorted_sfr[floor(n/3)];
sfr2 = sorted_sfr[floor(2*n/3)];
print("sfr tertiles: ", sfr1, " and ", sfr2);
bin1_indices = select(i -> sfr[i] < sfr1, [1..n]);
logmass_bin1 = vector(#bin1_indices, j, logmass[bin1_indices[j]]);
filtered_bin1 = filter_IQR(logmass_bin1);
K_bin1 = compute_K_theory(filtered_bin1);
kurtosis_bin1 = compute_kurtosis(logmass_bin1);
print("K_theory for sfr < ", sfr1, ": ", K_bin1);
print("Kurtosis for sfr < ", sfr1, ": ", kurtosis_bin1);
bin2_indices = select(i -> sfr[i] >= sfr1 && sfr[i] < sfr2, [1..n]);
logmass_bin2 = vector(#bin2_indices, j, logmass[bin2_indices[j]]);
filtered_bin2 = filter_IQR(logmass_bin2);
K_bin2 = compute_K_theory(filtered_bin2);
kurtosis_bin2 = compute_kurtosis(logmass_bin2);
print("K_theory for ", sfr1, " <= sfr < ", sfr2, ": ", K_bin2);
print("Kurtosis for ", sfr1, " <= sfr < ", sfr2, ": ", kurtosis_bin2);
bin3_indices = select(i -> sfr[i] >= sfr2, [1..n]);
logmass_bin3 = vector(#bin3_indices, j, logmass[bin3_indices[j]]);
filtered_bin3 = filter_IQR(logmass_bin3);
K_bin3 = compute_K_theory(filtered_bin3);
kurtosis_bin3 = compute_kurtosis(logmass_bin3);
print("K_theory for sfr >= ", sfr2, ": ", K_bin3);
print("Kurtosis for sfr >= ", sfr2, ": ", kurtosis_bin3);


# For ra
sorted_ra = vecsort(ra);
ra1 = sorted_ra[floor(n/3)];
ra2 = sorted_ra[floor(2*n/3)];
print("ra tertiles: ", ra1, " and ", ra2);
bin1_indices = select(i -> ra[i] < ra1, [1..n]);
logmass_bin1 = vector(#bin1_indices, j, logmass[bin1_indices[j]]);
filtered_bin1 = filter_IQR(logmass_bin1);
K_bin1 = compute_K_theory(filtered_bin1);
kurtosis_bin1 = compute_kurtosis(logmass_bin1);
print("K_theory for ra < ", ra1, ": ", K_bin1);
print("Kurtosis for ra < ", ra1, ": ", kurtosis_bin1);
bin2_indices = select(i -> ra[i] >= ra1 && ra[i] < ra2, [1..n]);
logmass_bin2 = vector(#bin2_indices, j, logmass[bin2_indices[j]]);
filtered_bin2 = filter_IQR(logmass_bin2);
K_bin2 = compute_K_theory(filtered_bin2);
kurtosis_bin2 = compute_kurtosis(logmass_bin2);
print("K_theory for ", ra1, " <= ra < ", ra2, ": ", K_bin2);
print("Kurtosis for ", ra1, " <= ra < ", ra2, ": ", kurtosis_bin2);
bin3_indices = select(i -> ra[i] >= ra2, [1..n]);
logmass_bin3 = vector(#bin3_indices, j, logmass[bin3_indices[j]]);
filtered_bin3 = filter_IQR(logmass_bin3);
K_bin3 = compute_K_theory(filtered_bin3);
kurtosis_bin3 = compute_kurtosis(logmass_bin3);
print("K_theory for ra >= ", ra2, ": ", K_bin3);
print("Kurtosis for ra >= ", ra2, ": ", kurtosis_bin3);
