M_t = M;
for(t = 1, 5, M_t = simulate_step(M_t, t); print("Time ", t, ": rank = ", matrank(M_t)));


\\ Step 5: Analyze
final_log_mass = vector(n, i, M_t[i,1]);
final_sfr = vector(n, i, M_t[i,2]);
final_met = vector(n, i, M_t[i,3]);
print("Avg log(mass): ", vecsum(final_log_mass)/n);
print("Avg SFR: ", vecsum(final_sfr)/n);
print("Avg metallicity: ", vecsum(final_met)/n);
