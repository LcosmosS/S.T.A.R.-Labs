import pandas as pd import numpy as np
# Load the data
df = pd.read_csv('Stellar_Mass2_Bigsby.csv')
# Filter out missing logmass values (marked as -9999)
df = df[df['logmass'] != -9999]
# Define redshift bins for grouping
sfr_bins = [-9999, -0.1, 0, 0.1, 1, 10] # Example bins, adjust based on data for i in range(len(sfr_bins) - 1): sfr_min = sfr_bins[i] sfr_max = sfr_bins[i+1] df_bin = df[(df['sfr'] >= sfr_min) & (df['sfr'] < sfr_max) & (df['sfr'] != -9999)] ...
# Function to compute K_theory
def compute_K_theory(log_mass): M = 10 ** log_mass M_sorted = np.sort(M) n = len(M) if n % 2 == 0: M0 = (M_sorted[n//2 - 1] + M_sorted[n//2]) / 2 else: M0 = M_sorted[n//2] sum_M_over_M0 = np.sum(M / M0) sum_M0_over_M = np.sum(M0 / M) K_theory = sum_M_over_M0 / sum_M0_over_M return K_theory
# Compute statistics for each z bin
