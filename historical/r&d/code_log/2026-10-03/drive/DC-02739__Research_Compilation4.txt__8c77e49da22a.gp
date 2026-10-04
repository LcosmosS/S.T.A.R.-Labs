  v = vector(N);
  for (i=1, N, {
    z = box_muller()[1];
    v[i] = mu + sigma * z;
