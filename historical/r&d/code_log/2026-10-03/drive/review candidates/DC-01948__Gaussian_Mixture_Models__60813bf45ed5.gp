final_log_mass = vector(n, i, M_t[i,1]);
final_sfr = vector(n, i, M_t[i,2]);
final_met = vector(n, i, M_t[i,3]);
print("Average log(mass): ", vecsum(final_log_mass)/n);
print("Average SFR: ", vecsum(final_sfr)/n);
print("Average metallicity: ", vecsum(final_met)/n);
