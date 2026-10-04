import numpy as np


# Assuming logmass and groups are NumPy arrays already defined
# Example: logmass = np.array([10.5, 9.2, 11.1, ...]), groups = np.array([0, 1, 1, ...])
logmass_group2 = logmass[groups == 1]


# Check what we extracted
print(f"Number of galaxies in Group 2: {len(logmass_group2)}")
print(f"Sample logmass values: {logmass_group2[:5]}")
