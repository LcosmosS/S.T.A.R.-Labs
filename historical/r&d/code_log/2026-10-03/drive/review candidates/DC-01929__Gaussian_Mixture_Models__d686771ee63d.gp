mass_sorted = vecsort(mass);


\\ Number of bins
B = 5;


\\ Number of elements
N = #mass_sorted;


\\ Elements per bin
elems_per_bin = floor(N / B);


\\ Bin endpoints
end_indices = vector(B, k, min(N, k * elems_per_bin));


\\ If N not divisible by B, adjust last bin
if (N % B != 0, end_indices[B] = N);


\\ Compute L_cosmo and rank
compute_L_cosmo(s) = {
  local(L_cosmo = 1, rank = 0, start, end, bin_M, M0_k, sum_M_over_M0, sum_M0_over_M, K, L_k);
  for(k = 1, B,
    start = if(k == 1, 1, end_indices[k-1] + 1);
    end = end_indices[k];
    bin_M = mass_sorted[start..end];
    M0_k = vecmedian(bin_M);
    sum_M_over_M0 = sum(i=1, #bin_M, bin_M[i] / M0_k);
    sum_M0_over_M = sum(i=1, #bin_M, M0_k / bin_M[i]);
    K = sum_M_over_M0 / sum_M0_over_M;
    if(abs(K - 1) < 0.2, rank = rank + 1);
    L_k = sum(i=1, #bin_M, (M0_k / bin_M[i])^s);
    L_cosmo = L_cosmo * L_k;
