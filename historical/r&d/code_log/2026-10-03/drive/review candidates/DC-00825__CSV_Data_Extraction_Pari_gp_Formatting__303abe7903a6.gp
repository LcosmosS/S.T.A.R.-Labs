  sorted_logmass = vecsort(logmass_subset);
  n = length(logmass_subset);
  Q1_index = floor(0.25 * (n + 1));
  Q3_index = floor(0.75 * (n + 1));
  Q1 = sorted_logmass[Q1_index];
  Q3 = sorted_logmass[Q3_index];
  IQR = Q3 - Q1;
  lower_bound = Q1 - 1.5 * IQR;
  upper_bound = Q3 + 1.5 * IQR;
  filtered_logmass = select(x -> x >= lower_bound && x <= upper_bound, logmass_subset);
  M = vector(length(filtered_logmass), i, 10^filtered_logmass[i]);
  sorted_M = vecsort(M);
  if (length(M) % 2 == 1,
    M0 = sorted_M[(length(M) + 1)/2],
    M0 = (sorted_M[length(M)/2] + sorted_M[length(M)/2 + 1]) / 2
