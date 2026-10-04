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


# Step 1: Refine Group 2’s Mass Distribution
group2_indices = (df['groups'] == 1)  # Group 2 is index 1
logmass_group2 = df[group2_indices]['logmass'].values
mass_group2 = 10 ** logmass_group2


# Test lognormal distribution
mean_logmass = np.mean(logmass_group2)
std_logmass = np.std(logmass_group2)
ks_stat_lognorm, p_value_lognorm = kstest(logmass_group2, 'norm', args=(mean_logmass, std_logmass))
print(f"KS test for lognormal distribution in Group 2: p-value = {p_value_lognorm:.4f}")


# Test exponential distribution on mass
expon_params = expon.fit(mass_group2)
ks_stat_expon, p_value_expon = kstest(mass_group2, 'expon', args=expon_params)
print(f"KS test for exponential distribution in Group 2: p-value = {p_value_expon:.4f}")


# Step 2: Optimize Adjustments for α and β
# Split data into training and validation sets
train_df, val_df = train_test_split(df, test_size=0.2, random_state=0)


# Function to compute adjusted K_theory
def adjusted_K_theory(logmass, density, sfr, alpha, beta):
    k_theory = compute_K_theory(logmass)
    return k_theory * (1 + alpha * density) * (1 + beta * sfr)


# Objective function to minimize MSE
def objective(params, logmass, density, sfr):
    alpha, beta = params
    k_adjusted = adjusted_K_theory(logmass, density, sfr, alpha, beta)
    return (k_adjusted - 1) ** 2


# Optimize α and β for each group
for group in range(5):
    group_train = train_df[train_df['groups'] == group]
    logmass_train = group_train['logmass'].values
    density_train = group_train['scaled_density'].mean() if 'scaled_density' in group_train else 0
    sfr_train = group_train['sfr'].median()
    
    # Initial guess for α and β
    initial_params = [0.1, 0.05]
    
    # Minimize the objective function
    result = minimize(objective, initial_params, args=(logmass_train, density_train, sfr_train))
    alpha_opt, beta_opt = result.x
    print(f"Group {group}: Optimized α = {alpha_opt:.4f}, β = {beta_opt:.4f}")


# Step 3: Validate on the validation set
for group in range(5):
    group_val = val_df[val_df['groups'] == group]
    logmass_val = group_val['logmass'].values
    density_val = group_val['scaled_density'].mean() if 'scaled_density' in group_val else 0
    sfr_val = group_val['sfr'].median()
    k_theory_val = compute_K_theory(logmass_val)
    k_adjusted_val = adjusted_K_theory(logmass_val, density_val, sfr_val, alpha_opt, beta_opt)
    print(f"Group {group}: Validation K_theory = {k_theory_val:.4f}, Adjusted K_theory = {k_adjusted_val:.4f}")


# Plot mass distribution for Group 2
plt.hist(logmass_group2, bins=30, density=True)
plt.title("Group 2 Stellar Mass Distribution")
plt.xlabel("logmass")
plt.ylabel("Density")
plt.savefig('group2_logmass_distribution.png')
plt.close()
print("Saved Group 2 logmass distribution as 'group2_logmass_distribution.png'.")


print("\nScript completed successfully!")
