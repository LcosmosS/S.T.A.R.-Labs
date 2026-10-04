import matplotlib.pyplot as plt
# Plot logmass distribution
plt.hist(df['logmass'], bins=50)
plt.title('Logmass Distribution')
plt.savefig('logmass_distribution.png')
