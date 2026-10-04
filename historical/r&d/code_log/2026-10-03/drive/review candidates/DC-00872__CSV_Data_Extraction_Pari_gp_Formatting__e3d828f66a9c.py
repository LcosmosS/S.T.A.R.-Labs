# Step 7: Extract 'z', 'sfr', and 'ra' for group averaging
z = valid_df['z'].values sfr = valid_df['sfr'].values ra = valid_df['ra'].values
# Step 8: Compute and print averages for each GMM group
for i in range(gmm.n_components): group_logmass = logmass[groups == i] group_z = z[groups == i] group_sfr = sfr[groups == i] group_ra = ra[groups == i] print(f"\nGroup {i}:") print(f" Average z = {np.mean(group_z):.4f}") print(f" Average sfr = {np.mean(group_sfr):.4f}") print(f" Average ra = {np.mean(group_ra):.4f}") print(f" Number of galaxies = {len(group_logmass)}")
print("\nScript completed successfully!")
def compute_K_theory(logmass_vec): M = 10 ** logmass_vec # Convert logmass to mass M_sorted = np.sort(M) n = len(M) if n == 0: return 0 # Median mass if n % 2 == 1: M0 = M_sorted[n // 2] else: M0 = (M_sorted[n // 2 - 1] + M_sorted[n // 2]) / 2 sum_M_over_M0 = np.sum(M / M0) sum_M0_over_M = np.sum(M0 / M) return sum_M_over_M0 / sum_M0_over_M
# Compute and print K_theory for each group
for i in range(gmm.n_components): group_logmass = logmass[groups == i] K_theory = compute_K_theory(group_logmass) print(f"Group {i}: K_theory = {K_theory:.4f}")
def compute_L_cosmo(logmass_vec, s): M = 10 ** logmass_vec M_sorted = np.sort(M) n = len(M) if n % 2 == 1: M0 = M_sorted[n // 2] else: M0 = (M_sorted[n // 2 - 1] + M_sorted[n // 2]) / 2 return np.sum((M0 / M) ** s)
# Compute L_cosmo at s=1 for each group
for i in range(gmm.n_components): group_logmass = logmass[groups == i] L_cosmo = compute_L_cosmo(group_logmass, 1) print(f"Group {i}: L_cosmo(s=1) = {L_cosmo:.4f}")
from scipy.stats import kstest, norm for i in range(gmm.n_components): group_logmass = logmass[groups == i] mean, std = np.mean(group_logmass), np.std(group_logmass) _, p_value = kstest(group_logmass, 'norm', args=(mean, std)) print(f"Group {i}: p-value for normality = {p_value:.4f}")
import matplotlib.pyplot as plt for i in range(3): plt.hist(logmass[groups == i], bins=50, density=True, alpha=0.6, label=f"Group {i}") plt.legend() plt.title(f"Logmass Distribution - Group {i}") plt.show()
