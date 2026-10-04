import matplotlib.pyplot as plt
plt.hist(valid_logmasses, bins=50, density=True)
plt.title('Histogram of log_mass for MyTable_Bigsby.csv')
plt.xlabel('log_mass (log10(M/M_sun))')
plt.ylabel('Density')
plt.show()
