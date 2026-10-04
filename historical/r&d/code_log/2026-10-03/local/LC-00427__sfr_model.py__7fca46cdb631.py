import pandas as pd
import numpy as np
from scipy.stats import gaussian_kde
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split, KFold
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.preprocessing import StandardScaler
import joblib

def calculate_k(masses):
    """Calculates the normalization constant K."""
    m0 = np.median(masses)
    sum_mi_m0 = np.sum(masses / m0)
    sum_m0_mi = np.sum(m0 / masses)
    return sum_mi_m0 / sum_m0_mi

def kde_l_function(data, s):
    """Computes the cosmological L-function using KDE."""
    kde = gaussian_kde(data[['logmass', 'z', 'petrorad_r']].values.T)
    
    # Generate grid of points
    logmass_range = np.linspace(data['logmass'].min(), data['logmass'].max(), 50)
    z_range = np.linspace(data['z'].min(), data['z'].max(), 50)
    petrorad_r_range = np.linspace(data['petrorad_r'].min(), data['petrorad_r'].max(), 50)
    
    # Evaluate KDE on the grid
    L_value = 0
    for logmass in logmass_range:
        for z in z_range:
            for petrorad_r in petrorad_r_range:
                density = kde(np.array([[logmass], [z], [petrorad_r]]))
                L_value += density * (10**logmass)**(-s)  # Corrected the L-function calculation
    return L_value

def estimate_rank(data):
    """Estimates the rank of the galaxy distribution."""
    l_at_1 = kde_l_function(data, 1)
    l_at_1_plus_delta = kde_l_function(data, 1.001)
    derivative = (l_at_1_plus_delta - l_at_1) / 0.001
    return 1 if np.abs(derivative) > 1e-5 else 2

def calculate_environment_density(data, n_neighbors=5):
    """Calculates local density using k-nearest neighbors."""
    from sklearn.neighbors import NearestNeighbors
    coords = data[['ra', 'dec']].values
    knn = NearestNeighbors(n_neighbors=n_neighbors)
    knn.fit(coords)
    distances, _ = knn.kneighbors(coords)
    return 1 / distances[:, -1]  # Inverse of distance to the 5th neighbor

def main():
    """Main function to execute the SFR prediction model."""
    # Load the data
    galaxy_data = pd.read_csv("Stellar_Mass2_Table_cleaned.csv")

    # Preprocess data: Fill missing values
    for col in ['logmass', 'z', 'dec', 'petrorad_r', 'sfr', 'ra']:  # Include 'ra' for environment calculation
        galaxy_data[col] = galaxy_data[col].fillna(galaxy_data[col].mean())

    # Calculate environment
    galaxy_data['environment'] = calculate_environment_density(galaxy_data)
    
    # Calculate K
    masses = 10**galaxy_data['logmass'].values  # Masses must be linear, not log
    K = calculate_k(masses)
    print(f"Normalization constant K: {K:.4f}")
    
    # Calculate L(1) using KDE
    galaxy_data['L_1'] = kde_l_function(galaxy_data, 1)
    print(f"L-function at s=1: {galaxy_data['L_1'].iloc[0]:.4f}")
    
    # Estimate rank
    rank = estimate_rank(galaxy_data)
    print(f"Estimated rank: {rank}")

    # Prepare data for Random Forest Regressor
    X = galaxy_data[['logmass', 'z', 'dec', 'petrorad_r', 'environment', 'L_1']]  # L_1 included
    y = galaxy_data['sfr']

    # Split data
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Standardize the features
    scaler = StandardScaler()
    X_train = scaler.fit_transform(X_train)
    X_test = scaler.transform(X_test)

    # Define and train the Random Forest Regressor
    model = RandomForestRegressor(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)

    # Predict SFR
    y_pred = model.predict(X_test)

    # Evaluate the model
    mse = mean_squared_error(y_test, y_pred)
    r2 = r2_score(y_test, y_pred)
    print(f"Mean Squared Error: {mse:.4f}")
    print(f"R-squared: {r2:.4f}")

    # K-Fold Cross-Validation
    kf = KFold(n_splits=5, shuffle=True, random_state=42)
    mse_list = []
    r2_list = []

    for fold, (train_index, test_index) in enumerate(kf.split(X, y)):
        X_train, X_test = X.iloc[train_index], X.iloc[test_index]
        y_train, y_test = y.iloc[train_index], y.iloc[test_index]
        
        # Scale the data for each fold
        X_train = scaler.fit_transform(X_train)
        X_test = scaler.transform(X_test)
        
        model.fit(X_train, y_train)  # Refit on each fold
        y_pred_fold = model.predict(X_test)
        
        mse_fold = mean_squared_error(y_test, y_pred_fold)
        r2_fold = r2_score(y_test, y_pred_fold)
        
        mse_list.append(mse_fold)
        r2_list.append(r2_fold)
        
        print(f"Fold {fold+1} MSE: {mse_fold:.4f}, R-squared: {r2_fold:.4f}")

    print(f"Average MSE: {np.mean(mse_list):.4f}")
    print(f"Average R-squared: {np.mean(r2_list):.4f}")

    # Save the model
    joblib.dump(model, 'sfr_prediction_model.joblib')

if __name__ == "__main__":
    main()
