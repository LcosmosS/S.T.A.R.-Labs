  v = vector(N);
  for (i=1, floor(N/2), {
    pair = box_muller();
    v[2*i-1] = mu + sigma * pair[1];
    if (2*i <= N, v[2*i] = mu + sigma * pair[2]);
