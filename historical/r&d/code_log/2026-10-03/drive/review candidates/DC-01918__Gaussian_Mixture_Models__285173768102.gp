mass = concat([mass_part1, mass_part2, mass_part3, mass_part4, mass_part5, mass_part6, mass_part7, mass_part8, mass_part9]);
M_sorted = vecsort(mass);
n = length(M_sorted);
num_bins = 5;
end_indices = vector(num_bins, k, floor((k / num_bins) * n));


compute_L_cosmo(s) = {
  my(L_cosmo = 1.0, rank = 0);
  for(k = 1, num_bins,
    my(start = if(k==1, 1, end_indices[k-1]+1), end = end_indices[k]);
    my(bin_M = M_sorted[start..end]);
    my(M0_k = median(bin_M));
    my(sum_M_over_M0 = sum(i=1, #bin_M, bin_M[i] / M0_k));
    my(sum_M0_over_M = sum(i=1, #bin_M, M0_k / bin_M[i]));
    my(K = sum_M_over_M0 / sum_M0_over_M);
    if(abs(K - 1) < 0.2, rank = rank + 1);
    my(L_k = sum(i=1, #bin_M, (M0_k / M_i)^s));
    L_cosmo = L_cosmo * L_k;
