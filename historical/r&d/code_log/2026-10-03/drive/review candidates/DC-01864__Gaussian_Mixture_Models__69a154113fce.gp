  if(length(v) == 0, return(0));
  local(n = length(v));
  local(sorted = vecsort(v));
  if(n % 2 == 1, sorted[(n+1)/2], (sorted[n/2] + sorted[n/2 + 1]) / 2);
}


indices = vector(5, k, select(i -> subpopulation[i] == k-1, [1..length(subpopulation)]));
M0 = vector(5, k, median(mass[indices[k]]));


log_L_k(k, s) = sum(i=1, length(indices[k]), s * log(M0[k] / mass[indices[k][i]]));
log_L_cosmo(s) = sum(k=1, 5, log_L_k(k, s));
L_cosmo(s) = exp(log_L_cosmo(s));


s = 1;
log_L_cosmo_s = log_L_cosmo(s);
L_cosmo_s = exp(log_L_cosmo_s);
print("L_cosmo(", s, ") = ", L_cosmo_s);
