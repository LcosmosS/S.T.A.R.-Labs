median_sfr = vecsort(sfr)[#sfr \ 2 + 1];
L_cosmo_weighted(s, M0, masses, sfr) = sum(i=1, #masses, (sfr[i] / median_sfr) * (M0 / masses[i])^s) / #masses;
L_weighted = L_cosmo_weighted(1, M0, masses, sfr);
