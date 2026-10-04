    gc.collect()


# Improved cosmic interweb plot
print("\nGenerating improved cosmic interweb plot...")
try:
    import matplotlib.pyplot as plt
    from mpl_toolkits.mplot3d import Axes3D

    from adjust_text import adjust_text
    interweb_data = [(a, b, rank, leading_coeff, omega, reg, tamagawa, weak_bsd_holds,
math.log(abs(E.discriminant())), math.log(E.conductor()),
                      (omega * reg * (VIRGO_DISTANCE / (omega * SQRT_KAPPA))**3) / (2.5e11 if
rank == 3 else 5e13 if rank == 2 else 1e15 if rank == 1 else 1e13))
