  masses = vector(n, i, 10^logmass_vec[i]);
  sorted_masses = vecsort(masses);
  m0 = sorted_masses[floor((n+1)/2)];
  sum_m_over_m0 = sum(i=1, n, masses[i] / m0);
  sum_m0_over_m = sum(i=1, n, m0 / masses[i]);
  k = sum_m_over_m0 / sum_m0_over_m;
