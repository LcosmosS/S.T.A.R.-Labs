M=vector(N,i,10^log_mass[i]); my_median(v)={my(sorted=vecsort(v));
my(len=length(sorted)); if(len%2==0,(sorted[len/2]+sorted[len/2+1])/2,sorted[(len+1)/2])};
M_0=10^my_median(log_mass); print("Reference mass M_0: ",M_0);
Reg_cosmo=sum(i=1,N,M[i]/M_0)/N; print("Reg_cosmo: ",Reg_cosmo);
prod_c_p_cosmo=N; print("prod_c_p_cosmo: ",prod_c_p_cosmo); Sha_cosmo=0.315;
print("Sha_cosmo: ",Sha_cosmo); T_cosmo=17; print("T_cosmo: ",T_cosmo);
L_cosmo(s)={sum(i=1,N,(M_0/M[i])^s)/N}; unscaled_left=L_cosmo(1); print("Unscaled
L_cosmo(1): ",unscaled_left);
right_side=(Omega_tildeReg_cosmoprod_c_p_cosmoSha_cosmo)/(T_cosmo^2);
print("Right side: ",right_side); K=right_side/unscaled_left; print("Normalization constant K:
