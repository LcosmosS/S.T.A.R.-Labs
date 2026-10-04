import matplotlib.pyplot as plt
plt.hist(df['logmass'], bins=50)
plt.title('Distribution of logmass')
   * plt.savefig('logmass_distribution.png')
   * Review saved plots (e.g., 'subpopulations.png', 'z_distributions.png') to assess clustering quality.
* Goal: Identify anomalies (e.g., outliers, invalid values) and confirm the physical meaningfulness of the clusters.
