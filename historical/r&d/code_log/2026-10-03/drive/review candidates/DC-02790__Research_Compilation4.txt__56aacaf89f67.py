import pandas as pd
import matplotlib.pyplot as plt
from scipy.stats import shapiro, skew, kurtosis


# Load the exported data
data = pd.read_csv("subgroup_z_0.05_0.1_low_sfr.txt", header=None)
log_mass = data[0]


# Plot histogram
plt.hist(log_mass, bins=30, density=True)
plt.title("Histogram of log_mass_low_sfr (z=0.05-0.1, low SFR)")
plt.xlabel("Log Stellar Mass")
plt.ylabel("Density")
plt.show()


# Compute statistics
mean = log_mass.mean()
std = log_mass.std()
skewness = skew(log_mass)
kurt = kurtosis(log_mass, fisher=True)  # Excess kurtosis
stat, p = shapiro(log_mass)


print(f"Mean: {mean}, Std: {std}, Skewness: {skewness}, Excess Kurtosis: {kurt}")
print(f"Shapiro test: stat={stat}, p-value={p}")  # p > 0.05 suggests normality
