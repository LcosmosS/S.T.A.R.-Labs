compute_modified_L = (s) -> {
  my(unique_subpops, unique_subpops_vec, L_mod, kk, k_val, masses_k_indices, masses_k, sorted_masses, n, M0_k, L_k_s);
  unique_subpops = Set(subpopulation);
  unique_subpops_vec = Vec(unique_subpops);
  L_mod = 1.0;
  for(kk=1, #unique_subpops_vec, {
    k_val = unique_subpops_vec[kk];
    masses_k_indices = select(i -> subpopulation[i] == k_val, [1..#mass]);
    masses_k = vector(#masses_k_indices, j, mass[masses_k_indices[j]]);
    sorted_masses = vecsort(masses_k);
    n = #sorted_masses;
    if (n % 2 == 1,
      M0_k = sorted_masses[(n+1)/2],
      M0_k = (sorted_masses[n/2] + sorted_masses[n/2 + 1]) / 2
    );
    L_k_s = sum(j=1, #masses_k, (M0_k / masses_k[j])^s) - 1;
    L_mod *= L_k_s;
