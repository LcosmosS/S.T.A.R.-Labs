s_values = vector(20, i, 0.1*i);
log_L_values = vector(#s_values, i, compute_log_L_cosmo(s_values[i]));
write("log_L_data.txt", s_values, log_L_values);
