for a, b in previous_curves:
    result = analyze_curve(a, b, conductor_limit=1e14)
    if len(result) == 10:
        success, features, rank, normalized_leading_coeff, omega, reg, tamagawa, weak_bsd_holds, E, selmer3_rank = result
        if success:
            results.append((None, (a, b, rank, normalized_leading_coeff, omega, reg, tamagawa, weak_bsd_holds, E, selmer3_rank)))
    gc.collect()


# Add the twisted curve (a=-102, b=918)
result = analyze_curve(-102, 918, conductor_limit=1e14)
if len(result) == 10:
    success, features, rank, normalized_leading_coeff, omega, reg, tamagawa, weak_bsd_holds, E, selmer3_rank = result
    if success:
        results.append((None, (a, b, rank, normalized_leading_coeff, omega, reg, tamagawa, weak_bsd_holds, E, selmer3_rank)))
gc.collect()


# Plot the cosmic interweb
print("\nGenerating cosmic interweb plot...")
try:
    import matplotlib.pyplot as plt
    from mpl_toolkits.mplot3d import Axes3D
    interweb_data = [(a, b, rank, leading_coeff, omega, reg, tamagawa, weak_bsd_holds, math.log(abs(E.discriminant())), math.log(E.conductor()))
                     for _, (a, b, rank, leading_coeff, omega, reg, tamagawa, weak_bsd_holds, E, _) in results if omega is not None]
    fig = plt.figure(figsize=(12, 10))
    ax = fig.add_subplot(111, projection='3d')
    ranks = [x[2] for x in interweb_data]
    log_deltas = [x[8] for x in interweb_data]
