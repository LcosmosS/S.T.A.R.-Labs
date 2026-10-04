import matplotlib.pyplot as plt
plt.figure(figsize=(10, 6))
for i in range(optimal_n):
    plt.hist(X[labels == i], bins=50, alpha=0.5, label=f'Subpopulation {i}')
plt.xlabel('log_mass')
plt.ylabel('Frequency')
plt.title('Galaxy Subpopulations Based on Stellar Mass')
plt.legend()
plt.savefig('subpopulations.png')
plt.close()
