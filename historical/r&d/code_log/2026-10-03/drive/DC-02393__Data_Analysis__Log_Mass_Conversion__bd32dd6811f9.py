# Define redshift bins for grouping
sfr_bins = [-9999, -0.1, 0, 0.1, 1, 10]  # Example bins, adjust based on data
for i in range(len(sfr_bins) - 1):
    sfr_min = sfr_bins[i]
    sfr_max = sfr_bins[i+1]
    df_bin = df[(df['sfr'] >= sfr_min) & (df['sfr'] < sfr_max) & (df['sfr'] != -9999)]
         *     ...
         * This loop is incomplete and will cause a syntax error, so removing it ensures the script runs, focusing on z bins as intended.
         5. Verify the Script Content:
         * Ensure the rest of the script is correct, including the compute_K_theory function and the loop for z bins, which computes statistics like K_{\text{theory}}, skewness, mean, and standard deviation for each bin. The corrected script should look like:
         * python
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
         * Save the file after ensuring all changes are made.
         6. Run the Script:
         * In the terminal, ensure you're in '/home/pmqr7/' by typing cd /home/pmqr7 and pressing Enter.
         * Ensure the virtual environment is activated with source /home/pmqr7/myenv/bin/activate if not already.
         * Type python analyze_galaxy_data.py and press Enter to run the script. This should now execute without the FileNotFoundError, printing statistics for each redshift bin.
         7. Interpret the Results:
         * The script will print statistics for each redshift bin, including the range (e.g., "0 to 0.05"), number of samples (n), K_{\text{theory}}, skewness, mean logmass, and standard deviation (sd) of logmass.
         * Look for bins where K_{\text{theory}} is closer to 1 and skewness is closer to 0, as these indicate a better fit to the log-normal distribution assumed in your theory. Compare with simulated data, where K_{\text{theory}} \approx 1.077 and skewness ≈ 0.0088, to assess data quality.
         * Note trends, such as whether K_{\text{theory}} improves at lower or higher redshifts, which could have cosmological implications, like galaxy evolution with distance.
         8. Optional: Save Results for Further Analysis:
         * Optionally, save the results to a new CSV for later use in PARI/GP or other tools by adding to the script:
         * python
results_df = pd.DataFrame(results)
         * results_df.to_csv('analysis_results.csv', index=False)
         * This creates "analysis_results.csv" in '/home/pmqr7/', which you can read in PARI/GP with read("analysis_results.csv") for further computations.
