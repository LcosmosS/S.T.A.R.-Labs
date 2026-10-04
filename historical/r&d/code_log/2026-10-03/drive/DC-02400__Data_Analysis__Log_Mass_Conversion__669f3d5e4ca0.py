import pandas as pd
import numpy as np


# Load the data
df = pd.read_csv('Stellar_Mass2_Table.csv')


# Filter out missing logmass values (marked as -9999)
df = df[df['logmass'] != -9999]


# Define redshift bins for grouping
z_bins = [0, 0.05, 0.1, 0.15, 0.2, 0.25, 0.3, 0.35, 0.4]


# Function to compute K_theory
def compute_K_theory(log_mass):
    M = 10 ** log_mass
    M_sorted = np.sort(M)
    n = len(M)
    if n % 2 == 0:
        M0 = (M_sorted[n//2 - 1] + M_sorted[n//2]) / 2
    else:
        M0 = M_sorted[n//2]
    sum_M_over_M0 = np.sum(M / M0)
    sum_M0_over_M = np.sum(M0 / M)
    K_theory = sum_M_over_M0 / sum_M0_over_M
    return K_theory


# Compute statistics for each z bin
results = []
for i in range(len(z_bins) - 1):
    z_min = z_bins[i]
    z_max = z_bins[i+1]
    df_bin = df[(df['z'] >= z_min) & (df['z'] < z_max)]
    if not df_bin.empty:
        log_mass = df_bin['logmass'].values
        K = compute_K_theory(log_mass)
        skewness = pd.Series(log_mass).skew()
        mean_logmass = np.mean(log_mass)
        sd_logmass = np.std(log_mass, ddof=1)
        results.append({
            'z_range': f'{z_min} to {z_max}',
            'n_samples': len(df_bin),
            'K_theory': K,
            'skewness': skewness,
            'mean_logmass': mean_logmass,
            'sd_logmass': sd_logmass
        })


# Print results
for result in results:
    print(f"z: {result['z_range']}, n={result['n_samples']}, K_theory={result['K_theory']:.4f}, "
          f"skewness={result['skewness']:.4f}, mean_logmass={result['mean_logmass']:.4f}, "
         *           f"sd_logmass={result['sd_logmass']:.4f}")
         * Ensure there are no incomplete loops or undefined variables, as seen in previous versions with sfr_bins, which should be removed if not used.
         5. Run the Script:
         * In the terminal, ensure you're in '/home/pmqr7/' by typing cd /home/pmqr7 and pressing Enter.
         * Type python analyze_galaxy_data.py and press Enter to run the script. This should now execute without the FileNotFoundError, printing statistics for each redshift bin, as seen in previous successful runs, such as:
