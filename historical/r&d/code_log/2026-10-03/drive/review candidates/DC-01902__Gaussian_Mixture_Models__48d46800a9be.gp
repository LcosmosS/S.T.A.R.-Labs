  if(#v == 0, return(0));
  v = vecsort(v);
  n = #v;
  if(n % 2 == 1, v[(n+1)/2], (v[n/2] + v[n/2 + 1]) / 2)
}


\\ Define compute_L_cosmo function
compute_L_cosmo(s) = {
  local(L_cosmo, rank, start, end, bin_M, M0_k, sum_M_over_M0, sum_M0_over_M, K, L_k);
  L_cosmo = 1;
  rank = 0;
  for(k = 1, 5,
    if(k == 1, start = 1, start = end_indices[k-1] + 1);
    end = end_indices[k];
    bin_M = M_sorted[start..end];
    M0_k = vecmedian(bin_M);
    sum_M_over_M0 = sum(i = 1, #bin_M, bin_M[i] / M0_k);
    sum_M0_over_M = sum(i = 1, #bin_M, M0_k / bin_M[i]);
    K = sum_M_over_M0 / sum_M0_over_M;
    if(abs(K - 1) < 0.2, rank = rank + 1);
    L_k = sum(i = 1, #bin_M, (M0_k / bin_M[i])^s);
    L_cosmo = L_cosmo * L_k
