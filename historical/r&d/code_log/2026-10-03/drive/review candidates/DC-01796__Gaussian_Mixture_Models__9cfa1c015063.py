import matplotlib.pyplot as plt
plt.figure(figsize=(10, 6))
for i in range(5):
    plt.hist(df[df['subpopulation'] == i]['logmass'], bins=50, alpha=0.5, label=f'Subpop {i}')
plt.legend()
plt.xlabel('logmass')
plt.ylabel('Frequency')
plt.title('Subpopulations based on logmass')
plt.savefig('subpopulations.png')
plt.close()
