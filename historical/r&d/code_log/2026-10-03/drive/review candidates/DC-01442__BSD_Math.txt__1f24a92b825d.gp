    k_val = unique_subpops_vec[kk];
masses_k_indices = select(i -> subpopulation[i] == k_val, [1..#mass]);
 masses_k = vector(#masses_k_indices, j, mass[masses_k_indices[j]]);
sorted_masses = vecsort(masses_k);
n = #sorted_masses;
if (n % 2 == 1,
 M0_k = sorted_masses[(n+1)/2],
      M0_k = (sorted_masses[n/2] + sorted_masses[n/2 + 1]) / 2
    );
 sum_term = sum(j=1, #masses_k, (M0_k / masses_k[j])^s);
 if (sum_term <= 0, error("Sum term is non-positive"));
log_L_k_s = log(sum_term);
log_L_cosmo_s += log_L_k_s;
