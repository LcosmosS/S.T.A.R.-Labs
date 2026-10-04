import pandas as pd
import numpy as np
from scipy.stats import gaussian_kde


print("Reading CSV...")
df = pd.read_csv("Stellar_Mass2_Table.csv")
print("CSV read successfully, shape:", df.shape)


print("Processing log_mass...")
log_mass = df['logmass'].replace(-9999, np.nan).dropna().values
print(f"Number of valid log_mass entries: {len(log_mass)}")


if len(log_mass) == 0:
    print("No valid log_mass data after filtering.")
else:
    print("Computing KDE...")
    kde = gaussian_kde(log_mass)
    density = kde(log_mass)
    threshold = density.max() * 0.01  # 1% of peak
    print(f"Threshold density: {threshold}")


    filtered_log_mass = log_mass[density > threshold]
    print(f"Number of filtered log_mass entries: {len(filtered_log_mass)}")


    print("Saving to filtered_log_mass.txt...")
    np.savetxt("filtered_log_mass.txt", filtered_log_mass, fmt='%.18f', header="log_mass = [", footer="];", comments='')
    print("File saved successfully.")
