import pandas as pd
import numpy as np
from sklearn.mixture import GaussianMixture
import matplotlib.pyplot as plt


# Load the log_mass data (assuming it's in a DataFrame)
# For demonstration, let's create a DataFrame from the provided log_mass range
log_mass = np.array([6.045, 11.659])  # Example range; replace with actual data
# Simulate or load your actual log_mass data (1,249 entries)
# For now, let's assume log_mass is already loaded as a list or array


# Convert to DataFrame
df = pd.DataFrame({'log_mass': log_mass})


# Outlier removal using IQR with stricter bounds (Q1 - 3*IQR, Q3 + 3*IQR)
Q1 = df['log_mass'].quantile(0.25)
Q3 = df['log_mass'].quantile(0.75)
IQR = Q3 - Q1
lower_bound = Q1 - 3 * IQR
upper_bound = Q3 + 3 * IQR


# Filter out outliers
df_filtered = df[(df['log_mass'] >= lower_bound) & (df['log_mass'] <= upper_bound)]
