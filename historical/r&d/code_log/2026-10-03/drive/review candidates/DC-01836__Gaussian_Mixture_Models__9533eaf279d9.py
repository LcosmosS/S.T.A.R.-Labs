import matplotlib.pyplot as plt


plt.figure(figsize=(10, 6))
for subpop in range(5):
    plt.hist(df[df['subpopulation'] == subpop]['logmass'], bins=50, alpha=0.5, label=f'Subpop {subpop}')
plt.xlabel('logmass')
plt.ylabel('Frequency')
plt.title('Subpopulations based on logmass')
plt.legend()
plt.savefig('subpopulations.png')
* plt.show()
