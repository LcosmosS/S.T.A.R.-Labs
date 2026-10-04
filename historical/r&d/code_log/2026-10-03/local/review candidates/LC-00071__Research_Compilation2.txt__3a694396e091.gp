median_sfr = vecsort(sfr)[#sfr \ 2 + 1];
* L_cosmo_weighted = sum(i=1, #masses, (sfr[i] / median_sfr) * (M0 / masses[i])) / #masses;
* Compute K_{\text{weighted}} = \frac{\text{Reg}_{\text{cosmo}}}{L_{\text{cosmo weighted}}}, testing if it stabilizes closer to 1.
* Subgroup Analysis: Filter galaxies based on properties, e.g., high ellipticity:
* gp
high_ellipticity_indices = select(i -> ellipticity[i] > median_ellipticity, [1..#masses]);
high_ellipticity_masses = vector(#high_ellipticity_indices, i, masses[high_ellipticity_indices[i]]);
L_high_ellipticity = sum(i=1, #high_ellipticity_masses, M0 / high_ellipticity_masses[i]) / #high_ellipticity_masses;
Reg_high_ellipticity = sum(i=1, #high_ellipticity_masses, high_ellipticity_masses[i] / M0) / #high_ellipticity_masses;
* K_high_ellipticity = Reg_high_ellipticity / L_high_ellipticity;
* Check if K_{\text{high ellipticity}} \approx 1, ensuring robustness across galaxy types.
