n = #data[1]/3;  // Assuming 3 values per galaxy, total length divisible by 3
log_mass = vector(n, i, data[1][3*i-2]);
sfr = vector(n, i, data[1][3*i-1]);
         * z = vector(n, i, data[1][3*i]);
