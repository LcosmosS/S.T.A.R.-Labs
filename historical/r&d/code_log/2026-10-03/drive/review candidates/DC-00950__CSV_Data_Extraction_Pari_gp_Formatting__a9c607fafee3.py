# Extract logmass for Group 2 (assuming Group 2 corresponds to group label 1)
logmass_group2 = df[df['groups'] == 1]['logmass'].values


# Alternatively, if 'groups' is a separate array:
# logmass_group2 = logmass[groups == 1]


print(f"Number of galaxies in Group 2: {len(logmass_group2)}")
print(f"Sample logmass values: {logmass_group2[:5]}")


# Step 2: Visualize the Mass Distribution
plt.hist(logmass_group2, bins=30, density=True)
plt.title("Logmass Distribution for Group 2")
plt.xlabel("logmass")
plt.ylabel("Density")
plt.savefig('group2_logmass_distribution.png')
print("Saved histogram as 'group2_logmass_distribution.png'.")


# Step 3: Test for Log-Normal Distribution (Normality of logmass)
mean = np.mean(logmass_group2)
std = np.std(logmass_group2)
ks_stat, p_value = kstest(logmass_group2, 'norm', args=(mean, std))
print(f"KS test p-value: {p_value:.4f}")


# Interpret the result
if p_value < 0.05:
    print("The logmass distribution for Group 2 does not follow a normal distribution (p < 0.05).")
else:
    print("The logmass distribution for Group 2 follows a normal distribution (p >= 0.05).")
