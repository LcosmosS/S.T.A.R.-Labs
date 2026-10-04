import matplotlib.pyplot as plt
plt.figure(figsize=(10, 6))
for i in range(5):
    subset = df[df['subpopulation'] == i]
    plt.hist(subset['z'], bins=30, alpha=0.5, label=f'Subpop {i}')
plt.legend()
plt.xlabel('Redshift (z)')
plt.ylabel('Frequency')
plt.title('Redshift Distribution by Subpopulation')
plt.savefig('z_distributions.png')
plt.close()


plt.figure(figsize=(10, 6))
for i in range(5):
    subset = df[df['subpopulation'] == i]
    plt.hist(subset['sfr'], bins=30, alpha=0.5, label=f'Subpop {i}')
plt.legend()
plt.xlabel('Star Formation Rate (sfr)')
plt.ylabel('Frequency')
plt.title('Star Formation Rate Distribution by Subpopulation')
plt.savefig('sfr_distributions.png')
plt.close()
