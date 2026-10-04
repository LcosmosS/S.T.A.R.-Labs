sfr_median = vecsort(sfr)[#sfr \ 2 + 1];
L_cosmo_weighted(s, M0, masses, sfr) = sum(i=1, #masses, if(sfr[i] != -9999, (sfr[i] / sfr_median) * (M0 / masses[i])^s, (M0 / masses[i])^s)) / #masses;
L_weighted = L_cosmo_weighted(1, M0, masses, sfr);
K_weighted = Reg_cosmo / L_weighted;
* print("K_weighted = ", K_weighted);
