# Improved cosmic interweb plot with Virgo Supercluster marker
print("\nGenerating improved cosmic interweb plot with Virgo Supercluster marker...")
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
    ranks = [float(x[2]) for x in interweb_data]
    log_deltas = [float(x[8]) for x in interweb_data]
