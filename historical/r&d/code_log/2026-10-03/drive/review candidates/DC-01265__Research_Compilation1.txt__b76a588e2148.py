import pandas as pd
import numpy as np
from scipy.stats import gaussian_kde
df = pd.read_csv("Stellar_Mass2_Table.csv")
log_mass = df['logmass'].replace(-9999, np.nan).dropna().values
kde = gaussian_kde(log_mass)
density = kde(log_mass)
threshold = density.max() * 0.01  # 1% of peak
filtered_log_mass = log_mass[density > threshold]
np.savetxt("/mnt/c/temp/filtered_log_mass.txt", filtered_log_mass, fmt='%.18f')  # Optional, for reference
formatted = "log_mass = [\n" + ",\n".join([f"{val:.18f}" for val in filtered_log_mass]) + "\n];"
print(formatted)
