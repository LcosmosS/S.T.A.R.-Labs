import numpy as np


# Parameters for a Schechter-like distribution
N = 10000  # Number of galaxies
M_star = 1e11  # Characteristic mass in solar masses
alpha = -1.0   # Schechter index
M_min = 1e9    # Minimum mass


# Generate masses
u = np.random.uniform(0, 1, N)
M_i = M_star * (1 - u) ** (1 / (alpha - 1))
Now you have an array M_i with N = 10,000 stellar masses.
