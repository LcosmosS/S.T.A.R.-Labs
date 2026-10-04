  v = vector(sample_size);
  for (i=1, floor(sample_size/2),
    pair = box_muller();
    v[2*i-1] = mean_val + std_val * pair[1];
    if (2*i <= sample_size, v[2*i] = mean_val + std_val * pair[2]);
