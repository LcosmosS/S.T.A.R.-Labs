import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split, KFold
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.preprocessing import StandardScaler
from scipy.stats import gaussian_kde
from sklearn.neighbors import NearestNeighbors
import joblib

def calculate_k(masses):
    """Calculates the normalization constant K."""
    m0 = np.median(masses)
    sum_mi_m0 = np.sum(masses / m0)
    sum_m0_mi = np.sum(m0 / masses)
    return sum_mi_m0 / sum_m0_mi

def kde_l_function(data, s):
    """Computes the cosmological L-function using KDE."""
    kde = gaussian_kde(data[['ra', 'dec', 'z']].values.T)
    
    # Generate grid of points
    ra_range = np.linspace(data['ra'].min(), data['ra'].max(), 50)
    dec_range = np.linspace(data['dec'].min(), data['dec'].max(), 50)
    z_range = np.linspace(data['z'].min(), data['z'].max(), 50)
    
    # Evaluate KDE on the grid
    L_value = 0
    for ra in ra_range:
        for dec in dec_range:
            for z1 in z_range:
                density = kde(np.array([[ra], [dec], [z1]]))
                L_value += density * (1 + z1)**(-s)
    return L_value

def estimate_rank(data):
    """Estimates the rank of the galaxy distribution."""
    l_at_1 = kde_l_function(data, 1)
    l_at_1_plus_delta = kde_l_function(data, 1.001)
    derivative = (l_at_1_plus_delta - l_at_1) / 0.001
    return 1 if np.abs(derivative) > 1e-5 else 2

def calculate_environment_density(data, n_neighbors=5):
    """Calculates local density using k-nearest neighbors."""
    coords = data[['ra', 'dec']].values
    knn = NearestNeighbors(n_neighbors=n_neighbors)
    knn.fit(coords)
    distances, _ = knn.kneighbors(coords)
    return 1 / distances[:, -1]

def main():
    """Main function to execute the model."""
    try:
        # Load the data
        galaxy_data = pd.read_csv("SDSSDR18_200000.csv")

        # Lowercase column names
        galaxy_data.columns = map(str.lower, galaxy_data.columns)
    
        #Renaming
        galaxy_data = galaxy_data.rename(columns={'redshift': 'z'})
    
        # Fill missing values in relevant columns
        for col in ['ra', 'dec', 'z']:
            galaxy_data[col] = galaxy_data[col].fillna(galaxy_data[col].mean())

        # Calculate environment density
        galaxy_data['environment'] = calculate_environment_density(galaxy_data)

        # Create logmass data from redshift using approximation
        H0 = 70  # Hubble constant
        c = 3e5  # speed of light km/s
        
        # Use .apply to calculate linear distance for each row
        galaxy_data['linear_distance'] = galaxy_data['z'].apply(lambda z: (c * z) / H0)

        # Calculate logmass using a single constant
        solar_mass_constant = 10**10
        galaxy_data['logmass'] = np.log10(galaxy_data['linear_distance'] * solar_mass_constant)


        # Calculate K
        masses = 10**galaxy_data['logmass'].values
        K = calculate_k(masses)
        print(f"Normalization constant K: {K:.4f}")

        #L-function
        galaxy_data['l_1'] = kde_l_function(galaxy_data, 1)
        print(f"L-function at s=1: {galaxy_data['l_1'].iloc[0]:.4f}")
        
        #Estimate Rank
        rank = estimate_rank(galaxy_data)
        print(f"Estimated rank: {rank}")

        # Prepare features and target
        X = galaxy_data[['ra', 'dec', 'z', 'environment', 'logmass', 'l_1']]
        y = galaxy_data['logmass']

        # Split data
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

        # Standardize the features
        scaler = StandardScaler()
        X_train = scaler.fit_transform(X_train)
        X_test = scaler.transform(X_test)

        # Define and train the Random Forest Regressor
        model = RandomForestRegressor(n_estimators=100, random_state=42)
        model.fit(X_train, y_train)

        # Predict logmass
        y_pred = model.predict(X_test)

        # Evaluate the model
        mse = mean_squared_error(y_test, y_pred)
        r2 = r2_score(y_test, y_pred)
        print(f"Mean Squared Error: {mse:.4f}")
        print(f"R-squared: {r2:.4f}")

        # 5-Fold Cross-Validation
        kf = KFold(n_splits=5, shuffle=True, random_state=42)
        mse_list = []
        r2_list = []

        for fold, (train_index, test_index) in enumerate(kf.split(X, y)):
            X_train, X_test = X.iloc[train_index], X.iloc[test_index]
            y_train, y_test = y.iloc[train_index], y.iloc[test_index]

            # Standardize each fold
            X_train = scaler.fit_transform(X_train)
            X_test = scaler.transform(X_test)

            model.fit(X_train, y_train)
            y_pred_fold = model.predict(X_test)

            mse_fold = mean_squared_error(y_test, y_pred_fold)
            r2_fold = r2_score(y_test, y_pred_fold)

            mse_list.append(mse_fold)
            r2_list.append(r2_fold)

            print(f"Fold {fold+1} MSE: {mse_fold:.4f}, R-squared: {r2_fold:.4f}")

        print(f"Average MSE: {np.mean(mse_list):.4f}")
        print(f"Average R-squared: {np.mean(r2_list):.4f}")

        # Save the model
        joblib.dump(model, 'galaxy_model.joblib')

    except FileNotFoundError:
        print("Error: The file 'SDSSDR18_200000.csv' was not found. Ensure it is in the correct directory.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    main()
