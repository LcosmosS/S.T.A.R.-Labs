    elif rank >= 2:
        return (alpha * logmass + beta * z + gamma * l_value + 
                delta * (l_value**2) + epsilon * dec + zeta * petrorad_r + 
                eta * environment + theta * (logmass * z))
    else:
        raise ValueError("Rank must be 1 or >=2")


# Load the data
galaxy_data = pd.read_csv("Stellar_Mass2_Table_cleaned.csv")  #  Ensure the correct path


# Preprocess data:  Fill missing values
for col in ['logmass', 'z', 'dec', 'petrorad_r', 'sfr']:
    galaxy_data[col] = galaxy_data[col].fillna(galaxy_data[col].mean())
    
if 'ra' in galaxy_data.columns and 'dec' in galaxy_data.columns:
    galaxy_data['environment'] = galaxy_data.groupby(['ra', 'dec'])['ra'].transform('size')
else:
    galaxy_data['environment'] = 0


# Calculate K
masses = galaxy_data['logmass'].values
K = calculate_k(masses)
print(f"Normalization constant K: {K:.4f}")


# Calculate L(1)
L_1 = cosmological_l_function(galaxy_data, 1)
print(f"L-function at s=1: {L_1:.4f}")


# Estimate rank
rank = estimate_rank(galaxy_data)
print(f"Estimated rank: {rank}")


# Prepare data for Random Forest Regressor
X = galaxy_data[['logmass', 'z', 'dec', 'petrorad_r', 'environment']] #Removed L_1
y = galaxy_data['sfr']


# Split data 
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)


# Define and train the Random Forest Regressor to optimize coefficients
model = RandomForestRegressor(random_state=42)
model.fit(X_train, y_train)


# Get the optimized coefficients
alpha, beta, gamma, delta, epsilon, zeta, eta, theta = 0,0,0,0,0,0,0,0 # Initialize.
if rank == 1:
    alpha, beta,  delta, epsilon, zeta, eta = model.feature_importances_  #first 6
elif rank >= 2:
    alpha, beta,  delta, epsilon, zeta, eta, theta = model.feature_importances_ # first 7
    
# Add L_1 separately, handling the case where rank might affect its usage.
if rank == 1:
    gamma = 0.1  # Example value, tune as needed.
elif rank >=2:
    gamma = 0.2
    
#SFR prediction
y_pred = []
for _, galaxy in X_test.iterrows():
    y_pred.append(predict_sfr(galaxy, L_1, rank))  # Use the calculated L_1
y_pred = np.array(y_pred)


# Evaluate the model
mse = mean_squared_error(y_test, y_pred)
