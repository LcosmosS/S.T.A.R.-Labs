  k_val = unique_subpops_vec[k];
  masses_k_indices = select(i -> subpopulation[i] == k_val, [1..#mass]);
  masses_k = vector(#masses_k_indices, j, mass[masses_k_indices[j]]);
  M0_k = vecmedian(masses_k);
  log_L_k_s = log(sum(j=1, #masses_k, (M0_k / masses_k[j])^s));
  log_L_cosmo_s += log_L_k_s;
