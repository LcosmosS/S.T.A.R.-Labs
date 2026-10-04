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
