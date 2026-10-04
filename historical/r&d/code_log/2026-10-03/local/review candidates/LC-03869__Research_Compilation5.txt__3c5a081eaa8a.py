print(f"Rank: {rank}")


# Print subpopulation counts
print(df['subpopulation'].value_counts())


# Plot histograms for 'logmass'
plt.figure(figsize=(10, 6))
for i in range(optimal_n):
    subset = df[df['subpopulation'] == i]
    plt.hist(subset['logmass'], bins=50, alpha=0.5, label=f'Subpop {i}')
plt.legend()
plt.xlabel('logmass')
plt.ylabel('Frequency')
plt.title('Subpopulations based on logmass')
plt.savefig('subpopulations.png')
plt.close()


# Plot histograms for 'z' (redshift)
plt.figure(figsize=(10, 6))
for i in range(optimal_n):
    subset = df[df['subpopulation'] == i]
    plt.hist(subset['z'], bins=30, alpha=0.5, label=f'Subpop {i}')
plt.legend()
plt.xlabel('Redshift (z)')
plt.ylabel('Frequency')
plt.title('Redshift Distribution by Subpopulation')
plt.savefig('z_distributions.png')
plt.close()


# Plot histograms for 'sfr' (star formation rate)
plt.figure(figsize=(10, 6))
for i in range(optimal_n):
    subset = df[df['subpopulation'] == i]
    plt.hist(subset['sfr'], bins=30, alpha=0.5, label=f'Subpop {i}')
plt.legend()
plt.xlabel('Star Formation Rate (sfr)')
plt.ylabel('Frequency')
plt.title('Star Formation Rate Distribution by Subpopulation')
plt.savefig('sfr_distributions.png')
plt.close()
