# Replace invalid data (-9999) with NaN and impute missing logmass values
df.replace(-9999, np.nan, inplace=True)
imputer = SimpleImputer(strategy='mean')
df['logmass'] = imputer.fit_transform(df[['logmass']])


# Verify required columns
required_columns = ['z', 'sfr', 'ra', 'dec', 'logmass']
if not all(col in df.columns for col in required_columns):
    print("Error: Missing required columns.")
    exit(1)


# Fit GMM to assign groups
gmm = GaussianMixture(n_components=5, random_state=0)
df['groups'] = gmm.fit_predict(df['logmass'].values.reshape(-1, 1))


# Define K_theory calculation
def compute_K_theory(logmass):
    M = 10 ** logmass
    M0 = np.median(M)
    return np.sum(M / M0) / np.sum(M0 / M)


### Step 1: Refine Group 2’s Mass Distribution
group2_data = df[df['groups'] == 1]['logmass'].values  # Group 2 is index 1
mass_group2 = 10 ** group2_data


# Test lognormal distribution
mean_logmass = np.mean(group2_data)
std_logmass = np.std(group2_data)
ks_stat_lognorm, p_value_lognorm = kstest(group2_data, 'norm', args=(mean_logmass, std_logmass))
print(f"Group 2 - Lognormal KS test p-value: {p_value_lognorm:.4f}")


# Test exponential distribution
expon_params = expon.fit(mass_group2)
ks_stat_expon, p_value_expon = kstest(mass_group2, 'expon', args=expon_params)
print(f"Group 2 - Exponential KS test p-value: {p_value_expon:.4f}")


### Step 2: Optimize Adjustments for α and β
# Split data into training and validation sets
train_df, val_df = train_test_split(df, test_size=0.2, random_state=0)


# Adjusted K_theory function
def adjusted_K_theory(logmass, density, sfr, alpha, beta):
    k_theory = compute_K_theory(logmass)
    return k_theory * (1 + alpha * density) * (1 + beta * sfr)


# Objective function for MSE minimization
def objective(params, logmass, density, sfr):
    alpha, beta = params
    k_adjusted = adjusted_K_theory(logmass, density, sfr, alpha, beta)
    return (k_adjusted - 1) ** 2  # Target K_theory = 1


# Optimize α and β per group
for group in range(5):
    group_train = train_df[train_df['groups'] == group]
    logmass_train = group_train['logmass'].values
    density_train = 0 if 'scaled_density' not in group_train else group_train['scaled_density'].mean()
    sfr_train = group_train['sfr'].median()
    
    # Optimize
    result = minimize(objective, [0.1, 0.05], args=(logmass_train, density_train, sfr_train))
    alpha_opt, beta_opt = result.x
    print(f"Group {group}: α = {alpha_opt:.4f}, β = {beta_opt:.4f}")


    # Validate
    group_val = val_df[val_df['groups'] == group]
    logmass_val = group_val['logmass'].values
    density_val = 0 if 'scaled_density' not in group_val else group_val['scaled_density'].mean()
    sfr_val = group_val['sfr'].median()
    k_theory_val = compute_K_theory(logmass_val)
    k_adjusted_val = adjusted_K_theory(logmass_val, density_val, sfr_val, alpha_opt, beta_opt)
    print(f"Group {group} Validation: K_theory = {k_theory_val:.4f}, Adjusted K_theory = {k_adjusted_val:.4f}")


# Plot Group 2’s mass distribution
plt.hist(group2_data, bins=30, density=True)
plt.title("Group 2 Logmass Distribution")
plt.xlabel("logmass")
plt.ylabel("Density")
plt.savefig('group2_logmass_distribution.png')
plt.close()
print("Saved Group 2 distribution plot.")


print("Script completed!")
