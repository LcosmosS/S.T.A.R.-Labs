  if(length(v) == 0, return(0));  /* Handle empty vector */
  local(n = length(v));
  local(sorted = vecsort(v));
  if(n % 2 == 1, sorted[(n+1)/2], (sorted[n/2] + sorted[n/2 + 1]) / 2);
}
