  if(n == 0, return(0));
  my(mean = sum(i=1, n, vec[i]) / n);
  my(centered = vector(n, i, vec[i] - mean));
  my(m2 = sum(i=1, n, centered[i]^2) / n);
  my(m4 = sum(i=1, n, centered[i]^4) / n);
  if(m2 == 0, return(0));
