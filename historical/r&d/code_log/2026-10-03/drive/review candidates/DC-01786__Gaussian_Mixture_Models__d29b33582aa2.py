import matplotlib.pyplot as plt
plt.figure()
for i in range(optimal_n):
    plt.hist(df[df['subpopulation'] == i]['logmass'], bins=50, alpha=0.5, label=f'Subpop {i}')
plt.legend()
plt.xlabel('logmass')
plt.ylabel('Frequency')
plt.title('Subpopulations based on logmass')
* plt.savefig('subpopulations.png')
