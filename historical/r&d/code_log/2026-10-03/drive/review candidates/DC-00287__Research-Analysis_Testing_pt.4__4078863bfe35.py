for a, b in previous_curves:
    result = analyze_curve(a, b, conductor_limit=1e14)
    if len(result) == 10:
        success, features, rank, normalized_leading_coeff, omega, reg, tamagawa, weak_bsd_holds, E, selmer3_rank = result
        if success:
            results.append((None, (a, b, rank, normalized_leading_coeff, omega, reg, tamagawa, weak_bsd_holds, E, selmer3_rank)))
    gc.collect()


# Twist the curve (a=34, b=-34) with d=5
print("\nTwisting curve (a=34, b=-34) to find a higher rank...")
d = 5
a_new = 34 * d
b_new = -34 * (d**3)
E_twist = EllipticCurve(QQ, [0, 0, 0, a_new, b_new])
print(f"Twisted curve: y² = x³ + {a_new}x + {b_new}")
try:
    result = analyze_curve(a_new, b_new, conductor_limit=1e14)
    if len(result) == 10:
        success, features, rank, normalized_leading_coeff, omega, reg, tamagawa, weak_bsd_holds, E, selmer3_rank = result
        if success:
            results.append(("Twist2", (a_new, b_new, rank, normalized_leading_coeff, omega, reg, tamagawa, weak_bsd_holds, E, selmer3_rank)))
            if selmer3_rank >= Integer(3):
                training_data.append(features)
                training_labels.append(selmer3_rank)
                print(f"Added twisted curve to training data: {features}, label: {selmer3_rank}")
except Exception as e:
    print(f"Failed to compute rank of twisted curve: {e}")


# Improved cosmic interweb plot with fixes for complex warnings
print("\nGenerating improved cosmic interweb plot...")
try:
    import matplotlib.pyplot as plt
    from mpl_toolkits.mplot3d import Axes3D
    interweb_data = []
    for _, (a, b, rank, leading_coeff, omega, reg, tamagawa, weak_bsd_holds, E, _) in results:
        if omega is not None:
            delta = float(E.discriminant())
            conductor = float(E.conductor())
            log_delta = math.log(abs(delta)) if delta != 0 else 0
            log_cond = math.log(abs(conductor)) if conductor != 0 else 0
            volume = float((omega * reg * (VIRGO_DISTANCE / (omega * SQRT_KAPPA))**3) / (1e12 if rank == 3 else 5e13 if rank == 2 else 1e15 if rank == 1 else 1e13))
            interweb_data.append((a, b, rank, leading_coeff, omega, reg, tamagawa, weak_bsd_holds, log_delta, log_cond, volume))
    
    fig = plt.figure(figsize=(14, 12))
    ax = fig.add_subplot(111, projection='3d')
    ranks = [float(x[2]) for x in interweb_data]  # Ensure real
    log_deltas = [float(x[8]) for x in interweb_data]
