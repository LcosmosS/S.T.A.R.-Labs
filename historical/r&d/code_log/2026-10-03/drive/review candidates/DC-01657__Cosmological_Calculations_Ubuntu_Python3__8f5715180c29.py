import pandas as pd
import numpy as np
from scipy.stats import gaussian_kde


# Load the original data
df = pd.read_csv('Stellar_Mass2_Table.csv')
log_mass = df['log_mass'].values


# Compute KDE
kde = gaussian_kde(log_mass)


# Evaluate density at each data point
density = kde(log_mass)


# Find the maximum density and set threshold to 10%
max_density = density.max()
threshold = 0.1 * max_density


# Filter the data points where density >= threshold
filtered_log_mass = log_mass[density >= threshold]


# Save the filtered log_mass to a file for PARI/GP
np.savetxt('filtered_log_mass_10pct.txt', filtered_log_mass, fmt='%.18f')
