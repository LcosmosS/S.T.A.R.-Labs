  sub_indices = randomsubset(1..#masses, N_sub);
  sub_masses = vector(N_sub, i, masses[sub_indices[i]]);
  L_sub = sum(i=1, N_sub, M0 / sub_masses[i]) / N_sub;
  Reg_sub = sum(i=1, N_sub, sub_masses[i] / M0) / N_sub;
  K_sub = Reg_sub / L_sub;
  return K_sub;
* }
* Compute for Multiple Subsamples: Compute K for 10 subsamples of 5,000 galaxies each:
* gp
K_subs = vector(10, i, subsample_K(masses, M0, 5000));
mean_K = vecsum(K_subs) / 10;
* std_K = sqrt(vecsum((K_subs - mean_K)^2) / 9);
* Expect mean_K ≈1 and small std_K, indicating stability.
