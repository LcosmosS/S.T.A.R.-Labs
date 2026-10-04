if(abs(left_side-right_side)<toleranceright_side,print("Cosmological BSD analogue holds
within 10%"),print("Cosmological BSD analogue fails: Left side != Right side")); N_sub=5;
log_mass_sub=vector(N_sub,i,log_mass[i]); M_sub=vector(N_sub,i,10^log_mass_sub[i]);
M_0_sub=10^my_median(log_mass_sub); print("Subsample M_0_sub: ",M_0_sub);
Reg_cosmo_sub=sum(i=1,N_sub,M_sub[i]/M_0_sub)/N_sub; print("Subsample
