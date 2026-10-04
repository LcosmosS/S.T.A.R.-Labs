import matplotlib.pyplot as plt


# Plot histograms of logmass for each subpopulation
plt.figure(figsize=(10, 6))
for i in range(optimal_n):
    plt.hist(df[df['subpopulation'] == i]['logmass'], bins=50, alpha=0.5, label=f'Subpopulation {i}')
plt.legend()
plt.xlabel('logmass')
plt.ylabel('Frequency')
plt.title('Subpopulations based on logmass')
plt.savefig('subpopulations.png')
plt.close()


# Plot BIC scores to confirm optimal number of components
plt.figure(figsize=(10, 6))
plt.plot(n_components_range, bic_scores, marker='o')
plt.xlabel('Number of components')
plt.ylabel('BIC score')
plt.title('BIC scores for different number of components')
plt.savefig('bic_scores.png')
plt.close()
