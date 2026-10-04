import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
interweb_data = [(a, b, rank, leading_coeff/10, omega, reg, tamagawa, weak_bsd_holds, math.log(abs(E.discriminant())), math.log(E.conductor())) for _, (a, b, rank, leading_coeff, omega, reg, tamagawa, weak_bsd_holds, E, _) in results if omega is not None]
fig = plt.figure(figsize=(12, 10))
ax = fig.add_subplot(111, projection='3d')
