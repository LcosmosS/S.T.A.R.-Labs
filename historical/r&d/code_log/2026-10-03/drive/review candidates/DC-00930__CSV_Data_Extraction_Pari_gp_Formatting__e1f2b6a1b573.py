import matplotlib.pyplot as plt
plt.hist(logmass[group2_indices], bins=30, density=True)
plt.title("Group 2 Stellar Mass Distribution")
plt.xlabel("logmass")
plt.ylabel("Density")
                  3. plt.show()
