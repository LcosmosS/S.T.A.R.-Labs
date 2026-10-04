from scipy import stats
logmass_group2 = ...  # extract logmass for Group 2
mean = np.mean(logmass_group2)
std = np.std(logmass_group2)
ks_stat, p_value = stats.kstest(logmass_group2, 'norm', args=(mean, std))
print(f"KS test p-value: {p_value}")
