  v = vector(N);
  for (k=1, N,
    z = box_muller()[1];
    v[k] = mu + sigma * z;
