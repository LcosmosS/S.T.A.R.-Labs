import pandas as pd
import numpy as np
from sklearn.mixture import GaussianMixture
from sklearn.impute import SimpleImputer
from sklearn.cluster import DBSCAN
from scipy.stats import kstest, gamma, norm
import matplotlib.pyplot as plt

# Define the file path
csv_file = 'Stellar_Mass2_Table.csv'

# Load the CSV file with error handling
try:
    df = pd.read_csv(csv_file)
    print(f"Successfully loaded '{csv_file}'.")
except FileNotFoundError:
    print(f"Error: The file '{csv_file}' was not found. Please ensure it is in the current directory.")
    exit(1)
except pd.errors.ParserError:
    print(f"Error: Could not parse '{csv_file}'. Please check the file format.")
    exit(1)

# Replace invalid data (-9999) with NaN
df.replace(-9999, np.nan, inplace=True)

# Verify required columns
required_columns = ['z', 'sfr', 'ra', 'dec', 'logmass']
missing_columns = [col for col in required_columns if col not in df.columns]
if missing_columns:
    print(f"Error: Missing columns in the CSV file: {missing_columns}")
    exit(1)

# Handle missing values in logmass with mean imputation
imputer = SimpleImputer(strategy='mean')
df['logmass'] = imputer.fit_transform(df[['logmass']])

# Fit Gaussian Mixture Model (GMM) with 5 components to logmass
try:
    gmm = GaussianMixture(n_components=5, random_state=0).fit(df['logmass'].values.reshape(-1, 1))
    df['groups'] = gmm.predict(df['logmass'].values.reshape(-1, 1))
    print(f"Fitted GMM with 5 components to 'logmass' data.")
except ValueError as e:
    print(f"Error: GMM fitting failed. Check 'logmass' data: {e}")
    exit(1)

# Define K_theory calculation function
def compute_K_theory(logmass_vec):
    M = 10 ** logmass_vec
    M0 = np.median(M)
    sum_M_over_M0 = np.sum(M / M0)
    sum_M0_over_M = np.sum(M0 / M)
    return sum_M_over_M0 / sum_M0_over_M

# Step 1: Analyze Mass Distribution for Group 2 (low-mass galaxies)
group2_indices = (df['groups'] == 1)  # Assuming Group 2 is index 1
logmass_group2 = df[group2_indices]['logmass'].values
mean, std = np.mean(logmass_group2), np.std(logmass_group2)
ks_stat, p_value = kstest(logmass_group2, 'norm', args=(mean, std))
print(f"KS test for normality of logmass in Group 2: p-value = {p_value:.4f}")

# If not normal, test gamma distribution
if p_value < 0.05:
    mass_group2 = 10 ** logmass_group2
    gamma_params = gamma.fit(mass_group2)
    ks_stat_gamma, p_value_gamma = kstest(mass_group2, 'gamma', args=gamma_params)
    print(f"KS test for gamma distribution in Group 2: p-value = {p_value_gamma:.4f}")

# Step 2: Incorporate Environmental Effects (clustering)
coords = df[['ra', 'dec']].values
dbscan = DBSCAN(eps=5, min_samples=10).fit(coords)
df['cluster'] = dbscan.labels_
df['local_density'] = df.groupby('cluster')['cluster'].transform('count')

# Step 3: Address Low SFR in Galaxy Evolution
for group in range(5):
    sfr_group = df[df['groups'] == group]['sfr'].dropna()
    print(f"Group {group}: Median SFR = {np.nanmedian(sfr_group):.4f}, "
          f"Mean SFR = {np.nanmean(sfr_group):.4f}")

# Step 4: Integrate Mass and Environmental Effects
df['mass_density_index'] = df['logmass'] * df['local_density']

# Step 5: Validate the Adjustments
for group in range(5):
    group_data = df[df['groups'] == group]
    k_theory = compute_K_theory(group_data['logmass'].values)
    avg_mass_density = np.mean(group_data['mass_density_index'])
    print(f"Group {group}: K_theory = {k_theory:.4f}, Avg Mass-Density Index = {avg_mass_density:.4f}")

# Plot mass distribution for Group 2
plt.hist(logmass_group2, bins=30, density=True)
plt.title("Group 2 Stellar Mass Distribution")
plt.xlabel("logmass")
plt.ylabel("Density")
plt.savefig('group2_logmass_distribution.png')
plt.close()
print("Saved Group 2 logmass distribution as 'group2_logmass_distribution.png'.")

print("\nScript completed successfully!")