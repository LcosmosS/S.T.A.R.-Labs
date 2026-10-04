import matplotlib.pyplot as plt
plt.hist(logmass_group2, bins=30, density=True)
plt.title("Logmass Distribution for Group 2")
plt.xlabel("logmass")
plt.ylabel("Density")
plt.show()
