import numpy as np
import pandas as pd


# Simulate stellar masses following a Schechter-like distribution
N = 10000  # Number of galaxies
M_star = 1e11  # Characteristic mass in solar masses
alpha = -1.0   # Schechter index
M_min = 1e9    # Minimum mass


# Generate masses using inverse transform sampling for Schechter function
u = np.random.uniform(0, 1, N)
M_i = M_star * (1 - u) ** (1 / (alpha - 1))


# Create a DataFrame
df = pd.DataFrame({'M_i': M_i})


# Calculate M_0 as the median mass
M_0 = np.median(df['M_i'])
