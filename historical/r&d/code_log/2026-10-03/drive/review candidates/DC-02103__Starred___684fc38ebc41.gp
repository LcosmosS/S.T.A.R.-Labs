  if(n == 0, return(0));  \\ Handle empty vectors
  my(mean = sum(i=1, n, v[i]) / n);
  my(m4 = sum(i=1, n, (v[i] - mean)^4) / n);
  my(m2 = sum(i=1, n, (v[i] - mean)^2) / n);
  if(m2 == 0, return(0), m4 / m2^2);  \\ Avoid division by zero
}


compute_K_theory(v) = {
  my(n = #v);
  if(n == 0, return(0));  \\ Handle empty vectors
  my(M = vector(n, i, 10^v[i]));  \\ Convert logmass to mass
  my(M0 = vecsort(M)[ceil(n/2)]);  \\ Median mass
  my(sum_Mi_M0 = sum(i=1, n, M[i] / M0));
  my(sum_M0_Mi = sum(i=1, n, M0 / M[i]));
  return(sum_Mi_M0 / sum_M0_Mi);
}


compute_subgroup_K_theory(vec_name) = {
  my(vec = eval(vec_name));  \\ Dynamically access the vector
  my(sorted_vec = vecsort(vec));
  my(n = #vec);
  my(v1 = sorted_vec[floor(n/3)], v2 = sorted_vec[floor(2*n/3)]);
  print(vec_name, " tertiles: ", v1, " and ", v2);


  my(bin1 = [], bin2 = [], bin3 = []);
  for(i = 1, n,
    if(vec[i] < v1, bin1 = concat(bin1, logmass[i]),
       vec[i] < v2, bin2 = concat(bin2, logmass[i]),
       bin3 = concat(bin3, logmass[i]))
