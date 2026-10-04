high_ellipticity_indices = select(i -> ellipticity[i] > median_ellipticity, [1..#masses]);
high_ellipticity_masses = vector(#high_ellipticity_indices, i, masses[high_ellipticity_indices[i]]);
L_high_ellipticity = sum(i=1, #high_ellipticity_masses, M0 / high_ellipticity_masses[i]) / #high_ellipticity_masses;
Reg_high_ellipticity = sum(i=1, #high_ellipticity_masses, high_ellipticity_masses[i] / M0) / #high_ellipticity_masses;
