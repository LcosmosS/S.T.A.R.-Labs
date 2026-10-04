K_subs = vector(10, i, subsample_K(masses, M0, 5000));
mean_K = vecsum(K_subs) / 10;
