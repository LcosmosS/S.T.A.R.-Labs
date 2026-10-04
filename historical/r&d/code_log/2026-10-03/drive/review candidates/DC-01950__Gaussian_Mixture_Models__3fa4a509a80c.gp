n = 1000;
mass = vector(n, i, 10^random(10.0));
sfr = vector(n, i, random(100.0));
metallicity = vector(n, i, 8.0 + random(2.0));


\\ Step 2: Preprocess
log_mass = vector(n, i, log(mass[i])/log(10));
sfr_max = vecmax(sfr); sfr_min = vecmin(sfr);
norm_sfr = vector(n, i, (sfr[i] - sfr_min) / (sfr_max - sfr_min));
met_max = vecmax(metallicity); met_min = vecmin(metallicity);
norm_met = vector(n, i, (metallicity[i] - met_min) / (met_max - met_min));


\\ Step 3: Define Matrix
M = matrix(n, 3);
for(i = 1, n, M[i,1] = log_mass[i]; M[i,2] = norm_sfr[i]; M[i,3] = norm_met[i]);
print("Initial rank: ", matrank(M));


\\ Step 4: Simulation
simulate_step(M, t) = {
  my(M_new = M);
  for(i = 1, n,
    M_new[i,2] = M[i,2] * exp(-t/10);
    M_new[i,3] = M[i,3] + 0.01 * t * M[i,1];
    if(M_new[i,2] < 0, M_new[i,2] = 0);
