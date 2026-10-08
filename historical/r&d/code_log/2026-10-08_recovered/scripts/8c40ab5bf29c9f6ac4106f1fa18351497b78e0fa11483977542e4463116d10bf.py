import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split, KFold
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error
import joblib

def calculate_k(masses):
    """
    Calculates the normalization constant K.

    Args:
        masses (list or numpy.ndarray): Array of galaxy stellar masses.

    Returns:
        float: The calculated normalization constant K.
    """
    m0 = np.median(masses)
    sum_mi_m0 = np.sum(masses / m0)
    sum_m0_mi = np.sum(m0 / masses)
    return sum_mi_m0 / sum_m0_mi

def cosmological_l_function(data, s):
    """
    Computes the cosmological L-function.

    Args:
        data (pd.DataFrame): DataFrame containing galaxy properties 
                              (logmass, z, petrorad_r).
        s (float): The complex variable s.

    Returns:
        float: The value of the L-function at s.
    """
    # Bin the data 
    bins = {}
    for index, row in data.iterrows():
        key = (row['logmass'], row['z'], row['petrorad_r'])
        if key not in bins:
            bins[key] = 0
        bins[key] += 1

    l_value = 0
    for i, count in enumerate(bins.values()):
        l_value += count * (i + 1)**(-s)  # Using i+1 as n
    return l_value

def estimate_rank(data):
    """
    Estimates the rank of the galaxy distribution.

    Args:
        data (pd.DataFrame): DataFrame containing galaxy properties 
                              (logmass, z, petrorad_r).

    Returns:
        int: Estimated rank (1 or 2).
    """
    l_at_1 = cosmological_l_function(data, 1)
    l_at_1_plus_delta = cosmological_l_function(data, 1.001)  #small delta
    derivative = (l_at_1_plus_delta - l_at_1) / 0.001
    
    if np.abs(derivative) > 1e-5:  # threshold
        return 1
    else:
        return 2

def predict_sfr(galaxy, l_value, rank):
    """
    Predicts the star formation rate (SFR) for a galaxy.

    Args:
        galaxy (pd.Series):  A single row from the galaxy DataFrame.
        l_value (float): The value of the cosmological L-function at s=1.
        rank (int): The estimated rank of the galaxy distribution.

    Returns:
        float: The predicted SFR.
    """
    logmass = galaxy['logmass']
    z = galaxy['z']
    dec = galaxy['dec']
    petrorad_r = galaxy['petrorad_r']
    environment = galaxy['environment']
    
    if rank == 1:
        return (alpha * logmass + beta * z + gamma * l_value + 
                delta * dec + epsilon * petrorad_r + zeta * environment + 
                eta * (logmass * z))
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
print(f"Mean Squared Error: {mse:.4f}")

# 5-Fold Cross-Validation
kf = KFold(n_splits=5, shuffle=True, random_state=42)
mse_list = []
for fold, (train_index, test_index) in enumerate(kf.split(X, y)):
    X_train, X_test = X.iloc[train_index], X.iloc[test_index]
    y_train, y_test = y.iloc[train_index], y.iloc[test_index]
    
    model.fit(X_train, y_train) # Refit
    
    y_pred_fold = []
    for _, galaxy in X_test.iterrows():
        y_pred_fold.append(predict_sfr(galaxy, L_1, rank))
    y_pred_fold = np.array(y_pred_fold)
    
    mse_fold = mean_squared_error(y_test, y_pred_fold)
    mse_list.append(mse_fold)
    print(f"Fold {fold+1} MSE: {mse_fold:.4f}")

print(f"Average MSE: {np.mean(mse_list):.4f}")

# Save the model
joblib.dump(model, 'sfr_prediction_model.joblib')