sfr_max = vecmax(sfr); sfr_min = vecmin(sfr);
norm_sfr = vector(n, i, (sfr[i] - sfr_min) / (sfr_max - sfr_min));
met_max = vecmax(metallicity); met_min = vecmin(metallicity);
norm_met = vector(n, i, (metallicity[i] - met_min) / (met_max - met_min));
