mean = np.mean(logmass_group2)
std = np.std(logmass_group2)
Then, use scipy.stats.kstest
from scipy.stats import kstest
ks_stat, p_value = kstest(logmass_group2, 'norm', args=(mean, std))
print("KS test p-value:", p_value)
