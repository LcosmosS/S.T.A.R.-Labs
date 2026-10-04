print(f"Rank: {rank}")


# Print subpopulation counts
print(df['subpopulation'].value_counts())


# Plot histograms
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


# ... (similar for other plots)
