# Step 3: Visualize the mass distribution
plt.hist(logmass_group2, bins=30, density=True)
plt.title("Group 2: Logmass Distribution")
plt.xlabel("logmass")
plt.ylabel("Density")
plt.savefig('group2_logmass_distribution.png')
plt.close()
print("Saved histogram as 'group2_logmass_distribution.png'.")


# Step 4: Test for normality using KS test
mean = np.mean(logmass_group2)
std = np.std(logmass_group2)
ks_stat, p_value = stats.kstest(logmass_group2, 'norm', args=(mean, std))
print(f"KS test for normality: statistic = {ks_stat:.4f}, p-value = {p_value:.4f}")
if p_value < 0.05:
    print("Logmass does not follow a normal distribution (reject normality).")
else:
    print("Logmass follows a normal distribution (fail to reject normality).")


# Step 5: Test a gamma distribution on mass (not logmass)
mass_group2 = np.exp(logmass_group2)  # Convert logmass to mass
gamma_params = stats.gamma.fit(mass_group2)
ks_stat_gamma, p_value_gamma = stats.kstest(mass_group2, 'gamma', args=gamma_params)
print(f"KS test for gamma distribution: statistic = {ks_stat_gamma:.4f}, p-value = {p_value_gamma:.4f}")


# Step 6: Test a power-law distribution on mass
fit = powerlaw.Fit(mass_group2, verbose=False)
print(f"Power-law fit: exponent = {fit.power_law.alpha:.4f}")
# Compare power-law to other distributions (e.g., lognormal)
R, p = fit.distribution_compare('power_law', 'lognormal')
print(f"Power-law vs lognormal: log-likelihood ratio = {R:.4f}, p-value = {p:.4f}")


# Step 7: Summary of findings
print("\nSummary of distribution tests for Group 2 mass:")
print(f"Normality of logmass (KS test): p-value = {p_value:.4f}")
print(f"Gamma distribution for mass (KS test): p-value = {p_value_gamma:.4f}")
print(f"Power-law vs lognormal for mass: R = {R:.4f}, p = {p:.4f}")
