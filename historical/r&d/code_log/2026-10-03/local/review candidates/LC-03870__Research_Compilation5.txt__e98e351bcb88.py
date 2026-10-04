import matplotlib.pyplot as plt
plt.hist(df['logmass'], bins=50)
plt.title('Distribution of logmass')
   * plt.savefig('logmass_distribution.png')
