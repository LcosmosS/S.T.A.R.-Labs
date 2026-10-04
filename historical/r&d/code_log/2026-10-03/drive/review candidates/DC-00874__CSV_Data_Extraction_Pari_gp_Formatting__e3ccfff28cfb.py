from scipy.stats import gamma
for i in range(3):
    params = gamma.fit(logmass[groups == i])
   *     print(f"Group {i} gamma fit: {params}")
