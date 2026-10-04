import matplotlib.pyplot as plt
for i in range(3):
    plt.hist(logmass[groups == i], bins=50, density=True, alpha=0.6, label=f"Group {i}")
    plt.legend()
    plt.title(f"Logmass Distribution - Group {i}")
   *     plt.show()
