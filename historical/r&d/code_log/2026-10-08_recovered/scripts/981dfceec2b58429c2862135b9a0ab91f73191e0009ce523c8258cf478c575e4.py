import pandas as pd
import numpy as np
from sklearn.mixture import GaussianMixture
import matplotlib.pyplot as plt
from scipy.stats import kstest, norm, gamma
import os

# Define file paths using os.path.join for cross-platform compatibility
csv_file = os.path.join(os.getcwd(), 'Stellar_Mass2_Table.csv')  # Input CSV file
pari_gp_dir = 'temp'  # Directory for PARI/GP file
pari_gp_file = os.path.join(pari_gp_dir, 'STM_Extract_Valid.gp')  # Output PARI/GP file

# Ensure the output directory exists
os.makedirs(pari_gp_dir, exist_ok=True)

# Define key columns to process
key_columns = ['ra', 'dec', 'z', 'logmass', 'sfr', 'petrorad_r', 'ellipticity']

# Step 1: Load the CSV file with error handling
try:
    df = pd.read_csv(csv_file)
    print(f"Successfully loaded '{csv_file}'.")
except FileNotFoundError:
    print(f"Error: The file '{csv_file}' was not found. Please ensure it is in the current directory.")
    exit(1)
except pd.errors.ParserError:
    print(f"Error: Could not parse '{csv_file}'. Please check the file format.")
    exit(1)

# Step 2: Verify all key columns exist in the DataFrame
missing_columns = [col for col in key_columns if col not in df.columns]
if missing_columns:
    print(f"Error: Missing columns in the CSV file: {missing_columns}")
    exit(1)

# Step 3: Filter out invalid data (NaN or -9999.0) in key columns
valid_df = df[df[key_columns].notna().all(axis=1) & (df[key_columns] != -9999.0).all(axis=1)]
print(f"Filtered data: {len(valid_df)} valid rows out of {len(df)} total rows.")

# Step 4: Write valid data to PARI/GP file
try:
    with open(pari_gp_file, 'w') as f:
        for col in key_columns:
            # Convert column values to float and then to string for PARI/GP compatibility
            values = ','.join(valid_df[col].astype(float).astype(str))
            f.write(f"{col}=[{values}];\n")
        # Include 'objid' if it exists (optional)
        if 'objid' in df.columns:
            objid_values = ','.join(valid_df['objid'].astype(str))
            f.write(f"objid=[{objid_values}];\n")
    print(f"Successfully wrote valid data to '{pari_gp_file}'.")
except PermissionError:
    print(f"Error: Permission denied when writing to '{pari_gp_file}'. Check directory permissions.")
    exit(1)
except Exception as e:
    print(f"Error: Failed to write to '{pari_gp_file}': {e}")
    exit(1)

# Step 5: Extract 'logmass' for GMM fitting
logmass = valid_df['logmass'].values

# Step 6: Optimize the number of GMM components using BIC
bic = []
for n in range(2, 6):
    gmm = GaussianMixture(n_components=n, random_state=0).fit(logmass.reshape(-1, 1))
    bic.append(gmm.bic(logmass.reshape(-1, 1)))
optimal_n = np.argmin(bic) + 2  # +2 because range starts at 2
print(f"Optimal number of components based on BIC: {optimal_n}")

# Step 7: Fit GMM with the optimal number of components
try:
    gmm = GaussianMixture(n_components=optimal_n, random_state=0).fit(logmass.reshape(-1, 1))
    groups = gmm.predict(logmass.reshape(-1, 1))
    print(f"Fitted GMM with {optimal_n} components to 'logmass' data.")
except ValueError as e:
    print(f"Error: GMM fitting failed. Check 'logmass' data: {e}")
    exit(1)

# Step 8: Extract 'z', 'sfr', and 'ra' for group averaging
z = valid_df['z'].values
sfr = valid_df['sfr'].values
ra = valid_df['ra'].values

# Step 9: Compute and print averages for each GMM group
for i in range(gmm.n_components):
    group_logmass = logmass[groups == i]
    group_z = z[groups == i]
    group_sfr = sfr[groups == i]
    group_ra = ra[groups == i]
    print(f"\nGroup {i}:")
    print(f"  Average z = {np.mean(group_z):.4f}")
    print(f"  Average sfr = {np.mean(group_sfr):.4f}")
    print(f"  Average ra = {np.mean(group_ra):.4f}")
    print(f"  Number of galaxies = {len(group_logmass)}")

# Step 10: Define K_theory computation
def compute_K_theory(logmass_vec):
    M = 10 ** logmass_vec  # Convert logmass to mass
    M_sorted = np.sort(M)
    n = len(M)
    if n == 0:
        return 0
    # Median mass
    if n % 2 == 1:
        M0 = M_sorted[n // 2]
    else:
        M0 = (M_sorted[n // 2 - 1] + M_sorted[n // 2]) / 2
    sum_M_over_M0 = np.sum(M / M0)
    sum_M0_over_M = np.sum(M0 / M)
    return sum_M_over_M0 / sum_M0_over_M

# Compute and print K_theory for each group
for i in range(gmm.n_components):
    group_logmass = logmass[groups == i]
    K_theory = compute_K_theory(group_logmass)
    print(f"Group {i}: K_theory = {K_theory:.4f}")

# Step 11: Define cosmic L-function computation
def compute_L_cosmo(logmass_vec, s):
    M = 10 ** logmass_vec
    M_sorted = np.sort(M)
    n = len(M)
    if n % 2 == 1:
        M0 = M_sorted[n // 2]
    else:
        M0 = (M_sorted[n // 2 - 1] + M_sorted[n // 2]) / 2
    return np.sum((M0 / M) ** s)

# Compute L_cosmo at s=1 for each group
for i in range(gmm.n_components):
    group_logmass = logmass[groups == i]
    L_cosmo = compute_L_cosmo(group_logmass, 1)
    print(f"Group {i}: L_cosmo(s=1) = {L_cosmo:.4f}")

# Step 12: Test for normality using Kolmogorov-Smirnov test
for i in range(gmm.n_components):
    group_logmass = logmass[groups == i]
    mean, std = np.mean(group_logmass), np.std(group_logmass)
    _, p_value = kstest(group_logmass, 'norm', args=(mean, std))
    print(f"Group {i}: p-value for normality = {p_value:.4f}")

# Step 13: Plot histograms for all groups and save as PNG
for i in range(gmm.n_components):
    plt.hist(logmass[groups == i], bins=50, density=True, alpha=0.6, label=f"Group {i}")
    plt.legend()
    plt.title(f"Logmass Distribution - Group {i}")
    plt.savefig(os.path.join(pari_gp_dir, f"Group_{i}_logmass.png"))
    plt.close()

# Step 14: Fit gamma distribution to each group
for i in range(gmm.n_components):
    params = gamma.fit(logmass[groups == i])
    print(f"Group {i} gamma fit: {params}")

# Step 15: Extended analysis of L_cosmo for s = 0.5, 1.5, 2
for s in [0.5, 1.5, 2]:
    for i in range(gmm.n_components):
        L = compute_L_cosmo(logmass[groups == i], s)
        print(f"Group {i}: L_cosmo(s={s}) = {L:.4f}")

# Step 16: Subgroup analysis for Group 1 (assuming Group 1 is of interest)
# Adjust the group index if needed based on results
group1_indices = groups == 1
z_group1 = z[group1_indices]
bins = np.percentile(z_group1, [0, 20, 40, 60, 80, 100])  # 5 bins
for i in range(len(bins) - 1):
    bin_mask = (z_group1 >= bins[i]) & (z_group1 < bins[i + 1])
    K = compute_K_theory(logmass[group1_indices][bin_mask])
    print(f"Group 1, z bin {i}: K_theory = {K:.4f}")

print("\nScript completed successfully!")