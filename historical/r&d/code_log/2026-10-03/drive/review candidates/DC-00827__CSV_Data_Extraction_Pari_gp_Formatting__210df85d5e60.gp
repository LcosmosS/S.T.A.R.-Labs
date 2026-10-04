n = length(logmass);
print("Number of entries: ", n);


// Full dataset
K_full = compute_K_theory(logmass);
print("Full dataset K_theory: ", K_full);


// For z
sorted_z = vecsort(z);
index1 = floor(0.33 * n);
index2 = floor(0.66 * n);
z_cutoff1 = sorted_z[index1];
z_cutoff2 = sorted_z[index2];
bin1_indices = select(i -> z[i] < z_cutoff1, [1..n]);
bin2_indices = select(i -> z[i] >= z_cutoff1 && z[i] < z_cutoff2, [1..n]);
bin3_indices = select(i -> z[i] >= z_cutoff2, [1..n]);
logmass_bin1 = vector(length(bin1_indices), j, logmass[bin1_indices[j]]);
K_bin1 = compute_K_theory(logmass_bin1);
print("z < ", z_cutoff1, ": K_theory = ", K_bin1);
logmass_bin2 = vector(length(bin2_indices), j, logmass[bin2_indices[j]]);
K_bin2 = compute_K_theory(logmass_bin2);
print(z_cutoff1, " <= z < ", z_cutoff2, ": K_theory = ", K_bin2);
logmass_bin3 = vector(length(bin3_indices), j, logmass[bin3_indices[j]]);
K_bin3 = compute_K_theory(logmass_bin3);
print("z >= ", z_cutoff2, ": K_theory = ", K_bin3);


// For sfr
sorted_sfr = vecsort(sfr);
index1 = floor(0.33 * n);
index2 = floor(0.66 * n);
sfr_cutoff1 = sorted_sfr[index1];
sfr_cutoff2 = sorted_sfr[index2];
bin1_indices = select(i -> sfr[i] < sfr_cutoff1, [1..n]);
bin2_indices = select(i -> sfr[i] >= sfr_cutoff1 && sfr[i] < sfr_cutoff2, [1..n]);
bin3_indices = select(i -> sfr[i] >= sfr_cutoff2, [1..n]);
logmass_bin1 = vector(length(bin1_indices), j, logmass[bin1_indices[j]]);
K_bin1 = compute_K_theory(logmass_bin1);
print("sfr < ", sfr_cutoff1, ": K_theory = ", K_bin1);
logmass_bin2 = vector(length(bin2_indices), j, logmass[bin2_indices[j]]);
K_bin2 = compute_K_theory(logmass_bin2);
print(sfr_cutoff1, " <= sfr < ", sfr_cutoff2, ": K_theory = ", K_bin2);
logmass_bin3 = vector(length(bin3_indices), j, logmass[bin3_indices[j]]);
K_bin3 = compute_K_theory(logmass_bin3);
print("sfr >= ", sfr_cutoff2, ": K_theory = ", K_bin3);


// For petrorad_r (re)
sorted_re = vecsort(petrorad_r);
index1 = floor(0.33 * n);
index2 = floor(0.66 * n);
re_cutoff1 = sorted_re[index1];
re_cutoff2 = sorted_re[index2];
bin1_indices = select(i -> petrorad_r[i] < re_cutoff1, [1..n]);
bin2_indices = select(i -> petrorad_r[i] >= re_cutoff1 && petrorad_r[i] < re_cutoff2, [1..n]);
bin3_indices = select(i -> petrorad_r[i] >= re_cutoff2, [1..n]);
logmass_bin1 = vector(length(bin1_indices), j, logmass[bin1_indices[j]]);
K_bin1 = compute_K_theory(logmass_bin1);
print("re < ", re_cutoff1, ": K_theory = ", K_bin1);
logmass_bin2 = vector(length(bin2_indices), j, logmass[bin2_indices[j]]);
K_bin2 = compute_K_theory(logmass_bin2);
print(re_cutoff1, " <= re < ", re_cutoff2, ": K_theory = ", K_bin2);
logmass_bin3 = vector(length(bin3_indices), j, logmass[bin3_indices[j]]);
K_bin3 = compute_K_theory(logmass_bin3);
print("re >= ", re_cutoff2, ": K_theory = ", K_bin3);
