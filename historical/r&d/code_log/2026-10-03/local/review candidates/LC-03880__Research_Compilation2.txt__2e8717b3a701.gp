  sub_indices = randomsubset(1..#masses, N_sub);
  sub_masses = vector(N_sub, i, masses[sub_indices[i]]);
  L_sub = sum(i=1, N_sub, M0 / sub_masses[i]) / N_sub;
  Reg_sub = sum(i=1, N_sub, sub_masses[i] / M0) / N_sub;
  K_sub = Reg_sub / L_sub;
  return K_sub;
