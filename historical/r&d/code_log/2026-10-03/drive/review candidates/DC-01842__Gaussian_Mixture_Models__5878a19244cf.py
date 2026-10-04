print(f"Rank with threshold 0.2: {rank}")


# Print subpopulation counts
print(df['subpopulation'].value_counts())


# Plot histogram for 'logmass' distribution
plt.figure(figsize=(10, 6))
plt.hist(df['logmass'], bins=50)
plt.title('Distribution of logmass')
plt.xlabel('logmass')
plt.ylabel('Frequency')
plt.savefig('logmass_distribution.png')
plt.close()


# Plot histograms for 'logmass' by subpopulation
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


# Plot histograms for 'z' (redshift) by subpopulation
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


# Plot histograms for 'sfr' (star formation rate) by subpopulation
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
