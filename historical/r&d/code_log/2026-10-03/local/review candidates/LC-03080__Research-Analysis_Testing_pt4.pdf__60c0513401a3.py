gc.collect()

# Plot the cosmic interweb
print("\nGenerating cosmic interweb plot...")
try:
    import matplotlib.pyplot as plt
    from mpl_toolkits.mplot3d import Axes3D
    interweb_data = [(a, b, rank, leading_coeff, omega, reg, tamagawa, weak_bsd_holds,
math.log(abs(E.discriminant())), math.log(E.conductor()))
