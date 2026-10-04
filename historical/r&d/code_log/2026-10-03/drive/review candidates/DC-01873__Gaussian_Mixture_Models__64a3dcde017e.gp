log_mass_sorted = vecsort(log_mass);


/* Compute masses M_i = 10^log_mass_i */
n = #log_mass;
M_sorted = vector(n, i, 10^log_mass_sorted[i]);


/* Define bin end indices (5 bins with ~equal numbers of galaxies) */
end_indices = vector(5, k, floor((k / 5) * n));


/* Function to compute L_cosmo(s) and rank */
compute_L_cosmo(s) = {
  local(L_cosmo = 1, rank = 0);
  for (k = 1, 5,
    start = if(k == 1, 1, end_indices[k-1] + 1);
    end = end_indices[k];
    bin_M = M_sorted[start..end];
    M0_k = vecmedian(bin_M);  /* Median mass in the bin */
    /* Compute K for rank */
    sum_M_over_M0 = sum(i = 1, #bin_M, bin_M[i] / M0_k);
    sum_M0_over_M = sum(i = 1, #bin_M, M0_k / bin_M[i]);
    K = sum_M_over_M0 / sum_M0_over_M;
    if (abs(K - 1) < 0.2, rank = rank + 1);
    /* Compute L_k(s) */
    L_k = sum(i = 1, #bin_M, (M0_k / bin_M[i])^s);
    L_cosmo = L_cosmo * L_k;
