import matplotlib.pyplot as plt
plt.figure(figsize=(10, 6))
for i in range(5):
    subset = df[df['subpopulation'] == i]
    plt.hist(subset['logmass'], bins=50, alpha=0.5, label=f'Subpopulation {i}')
plt.xlabel('log_mass')
plt.ylabel('Frequency')
plt.title('Galaxy Subpopulations Based on Stellar Mass')
plt.legend()
plt.savefig('subpopulations.png')
plt.close()