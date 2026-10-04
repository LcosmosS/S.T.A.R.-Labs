import pandas as pd
import matplotlib.pyplot as plt
from scipy.stats import shapiro, skew, kurtosis


data = pd.read_csv("subgroup_z_0.05_0.1_low_sfr.txt", header=None)
plt.hist(data[0], bins=30, density=True)
plt.title("Histogram of log_mass_low_sfr (z=0.05-0.1, low SFR)")
plt.show()


mean = data[0].mean()
std = data[0].std()
skewness = skew(data[0])
kurt = kurtosis(data[0], fisher=True)  # Excess kurtosis
stat, p = shapiro(data[0])
print(f"Mean: {mean}, Std: {std}, Skewness: {skewness}, Excess Kurtosis: {kurt}")
                                                                     * print(f"Shapiro test: stat={stat}, p-value={p}")  # p > 0.05 suggests normality
                                                                     * Compare these stats (mean ~10, std ~1, skewness ~0, kurtosis ~0) to your simulated data expectations.
                                                                     2. Investigate Discrepancies:
                                                                     * Simulated K_theory (0.998) is slightly below 1, while real data (1.0036) is slightly above. This could reflect sample size effects or real data deviations (e.g., excess kurtosis of 3.68). The exported data analysis will clarify this.
                                                                     3. Robustness Check:
                                                                     * Test other redshift bins or datasets (e.g., "Stellar_Mass2_Bigsby.csv") to ensure consistency.
