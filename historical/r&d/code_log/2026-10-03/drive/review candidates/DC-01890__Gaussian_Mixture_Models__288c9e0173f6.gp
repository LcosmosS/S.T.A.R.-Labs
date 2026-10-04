log_mass = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10];
log_mass_sorted = vecsort(log_mass);
n = #log_mass;
M_sorted = vector(n, i, 10^log_mass_sorted[i]);
end_indices = vector(5, k, floor((k / 5) * n));


/* Function definition */
compute_L_cosmo(s) = {
  local(L_cosmo, rank, start, end, bin_M, M0_k, sum_M_over_M0, sum_M0_over_M, K, L_k);
  L_cosmo = 1;
  rank = 0;
  for(k=1, 5,
    if(k==1, start=1, start=end_indices[k-1]+1);
    end=end_indices[k];
    bin_M=M_sorted[start..end];
    M0_k=vecmedian(bin_M);
    sum_M_over_M0=sum(i=1, #bin_M, bin_M[i]/M0_k);
    sum_M0_over_M=sum(i=1, #bin_M, M0_k/bin_M[i]);
    K=sum_M_over_M0 / sum_M0_over_M;
    if(abs(K-1)<0.2, rank=rank+1);
    L_k=sum(i=1, #bin_M, (M0_k / bin_M[i])^s);
    L_cosmo=L_cosmo * L_k
