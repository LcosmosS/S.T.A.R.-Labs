t_H=1.44e10; Omega_cosmo=1.38e10; \nOmega_tilde=Omega_cosmo/t_H;
print("Omega_tilde: ", Omega_tilde); \nread("C:\\temp\\data_extract.txt"); if
(#log_mass != 1000, error("log_mass does not have \n1000 entries")); N=1000;
M=vector(N,i,10^log_mass[i]); M_0=vecmedian(M); \nprint("Reference mass M_0: ",
