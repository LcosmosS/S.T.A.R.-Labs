for a, b in previous_curves:
    result = analyze_curve(a, b, conductor_limit=1e14)
    if len(result) == 10:
        success, features, rank, normalized_leading_coeff, omega, reg, tamagawa, weak_bsd_holds, E, selmer3_rank = result
        if success:
            results.append((None, (a, b, rank, normalized_leading_coeff, omega, reg, tamagawa, weak_bsd_holds, E, selmer3_rank)))
    gc.collect()


# Twist the curve (a=-1597, b=987) with d=3
print("\nTwisting curve (a=-1597, b=987) to find a higher rank...")
d = 3
a_new = -1597 * d
b_new = 987 * (d**3)
E_twist = EllipticCurve(QQ, [0, 0, 0, a_new, b_new])
print(f"Twisted curve: y² = x³ + {a_new}x + {b_new}")
try:
    result = analyze_curve(a_new, b_new, conductor_limit=1e14)
    if len(result) == 10:
        success, features, rank, normalized_leading_coeff, omega, reg, tamagawa, weak_bsd_holds, E, selmer3_rank = result
        if success:
            results.append(("Twist", (a_new, b_new, rank, normalized_leading_coeff, omega, reg, tamagawa, weak_bsd_holds, E, selmer3_rank)))
            if selmer3_rank >= Integer(3):
                training_data.append(features)
                training_labels.append(selmer3_rank)
                print(f"Added twisted curve to training data: {features}, label: {selmer3_rank}")
except Exception as e:
    print(f"Failed to compute rank of twisted curve: {e}")


# Improved cosmic interweb plot without adjust_text
print("\nGenerating improved cosmic interweb plot...")
try:
    import matplotlib.pyplot as plt
    from mpl_toolkits.mplot3d import Axes3D
    interweb_data = [(a, b, rank, leading_coeff, omega, reg, tamagawa, weak_bsd_holds, math.log(abs(E.discriminant())), math.log(E.conductor()),
                      (omega * reg * (VIRGO_DISTANCE / (omega * SQRT_KAPPA))**3) / (1e12 if rank == 3 else 5e13 if rank == 2 else 1e15 if rank == 1 else 1e13))
                     for _, (a, b, rank, leading_coeff, omega, reg, tamagawa, weak_bsd_holds, E, _) in results if omega is not None]
    fig = plt.figure(figsize=(14, 12))
    ax = fig.add_subplot(111, projection='3d')
    ranks = [x[2] for x in interweb_data]
    log_deltas = [x[8] for x in interweb_data]
