print("Precision set to 38");
t_H = 1.44e10;
Omega_cosmo = 1.38e10;
Omega_tilde = Omega_cosmo / t_H;
print("Omega_tilde: ", Omega_tilde);
log_mass = [10.29471, 11.36537, 10.56586, 9.363875, 11.16167, 11.16527, 9.958716, 10.3831, 9.767632];
z = [0.02122228, 0.02037833, 0.06465632, 0.05265425, 0.2138606, 0.1212705, 0.05598059, 0.09708638, 0.06477907];
N = length(log_mass);
print("Number of galaxies N: ", N);
M = vector(N, i, 10^log_mass[i]);
my_median(v) = {
    my(sorted = vecsort(v));
    my(len = length(sorted));
    if(len % 2 == 0,
        (sorted[len/2] + sorted[len/2 + 1]) / 2,
        sorted[(len+1)/2]
