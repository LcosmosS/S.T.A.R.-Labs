for a, b in previous_curves:
    result = analyze_curve(a, b, conductor_limit=1e14)
    if len(result) == 10:
        success, features, rank, normalized_leading_coeff, omega, reg, tamagawa, weak_bsd_holds, E, selmer3_rank = result
        if success:
            results.append((None, (a, b, rank, normalized_leading_coeff, omega, reg, tamagawa, weak_bsd_holds, E, selmer3_rank)))
    gc.collect()


# Improved cosmic interweb plot
print("\nGenerating improved cosmic interweb plot...")
try:
    import matplotlib.pyplot as plt
    from mpl_toolkits.mplot3d import Axes3D
    from adjust_text import adjust_text
    interweb_data = [(a, b, rank, leading_coeff, omega, reg, tamagawa, weak_bsd_holds, math.log(abs(E.discriminant())), math.log(E.conductor()),
                      (omega * reg * (VIRGO_DISTANCE / (omega * SQRT_KAPPA))**3) / (2.5e11 if rank == 3 else 5e13 if rank == 2 else 1e15 if rank == 1 else 1e13))
                     for _, (a, b, rank, leading_coeff, omega, reg, tamagawa, weak_bsd_holds, E, _) in results if omega is not None]
    fig = plt.figure(figsize=(14, 12))
    ax = fig.add_subplot(111, projection='3d')
    ranks = [x[2] for x in interweb_data]
    log_deltas = [x[8] for x in interweb_data]
