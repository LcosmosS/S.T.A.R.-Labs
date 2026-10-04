import matplotlib.pyplot as plt
import numpy as np
data = np.loadtxt("log_L_data.txt")
s_vals, log_L_vals = data[:, 0], data[:, 1]
plt.plot(s_vals, log_L_vals)
plt.xlabel('s')
plt.ylabel('log L_cosmo(s)')
plt.title('Logarithmic Cosmological L-function vs s')
plt.savefig('log_L_cosmo_plot.png')
plt.close()
Computing the Derivative at s=1
