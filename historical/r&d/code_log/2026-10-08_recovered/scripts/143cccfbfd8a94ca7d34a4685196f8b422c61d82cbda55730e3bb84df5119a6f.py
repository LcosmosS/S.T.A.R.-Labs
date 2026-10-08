import pandas as pd
import numpy as np
from scipy.stats import gaussian_kde
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor, VotingRegressor
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.neighbors import KDTree
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
import joblib

def calculate_k(masses):
    """Calculate normalization constant K with error handling."""
    m0 = np.median(masses)
    with np.errstate(divide='ignore', invalid='ignore'):
        ratio = masses / m0
        inv_ratio = m0 / masses
    return np.nansum(ratio) / np.nansum(inv_ratio)

def kde_l_function(data, s_values):
    """Compute L-function using KDE for continuous distribution."""
    points = data[['logmass', 'z', 'petrorad_r']].values.T
    kde = gaussian_kde(points)
    
    # Generate integration grid
    grid = np.meshgrid(np.linspace(data['logmass'].min(), data['logmass'].max(), 50),
                       np.linspace(data['z'].min(), data['z'].max(), 50),
                       np.linspace(data['petrorad_r'].min(), data['petrorad_r'].max(), 50))
    grid_points = np.vstack([g.ravel() for g in grid])
    
    # Evaluate KDE and integrate
    densities = kde(grid_points)
    l_values = []
    for s in s_values:
        integrand = densities * (grid_points[0] ** -s)  # logmass component
        l_values.append(np.trapz(integrand, grid_points[0]))
    return l_values

def estimate_rank(data):
    """Robust rank estimation using curve fitting."""
    s_values = np.linspace(0.95, 1.05, 11)
    l_values = kde_l_function(data, s_values)
    
    # Fit quadratic polynomial to estimate derivative at s=1
    coeffs = np.polyfit(s_values - 1, l_values, 2)
    derivative = 2 * coeffs[0] * (0) + coeffs[1]  # dy/ds at s=1
    
    return 1 if abs(derivative) > 1e-4 else 2

def calculate_environment_density(data, n_neighbors=5):
    """Calculate local density using k-nearest neighbors."""
    coords = data[['ra', 'dec', 'z']].values
    tree = KDTree(coords)
    distances, _ = tree.query(coords, k=n_neighbors+1)
    return 1 / distances[:,-1]  # Inverse of distance to 5th neighbor

def main():
    # Load and prepare data
    data = pd.read_csv("Stellar_Mass2_Table_cleaned.csv")
    
    # Preprocessing
    for col in ['logmass', 'z', 'dec', 'petrorad_r', 'sfr']:
        data[col] = data[col].fillna(data[col].median())
    
    data['environment'] = calculate_environment_density(data)
    data['logmass_z_interaction'] = data['logmass'] * data['z']
    
    # Calculate BSD-inspired features
    masses = 10**data['logmass']  # Convert logmass to linear scale
    data['K'] = calculate_k(masses)
    data['rank'] = estimate_rank(data)
    data['L_1'] = kde_l_function(data, [1.0])[0]
    
    # Prepare features
    features = ['logmass', 'z', 'dec', 'petrorad_r', 'environment',
                'logmass_z_interaction', 'K', 'L_1', 'rank']
    X = data[features]
    y = data['sfr']
    
    # Split data
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # Define models with preprocessing pipeline
    rf = Pipeline([
        ('scaler', StandardScaler()),
        ('model', RandomForestRegressor(n_estimators=200, random_state=42))
    ])
    
    gbm = Pipeline([
        ('scaler', StandardScaler()),
        ('model', GradientBoostingRegressor(n_estimators=300, random_state=42))
    ])
    
    # Combined model
    ensemble = VotingRegressor([
        ('rf', rf),
        ('gbm', gbm)
    ])
    
    # Hyperparameter grid
    param_grid = {
        'rf__model__max_depth': [None, 10],
        'gbm__model__learning_rate': [0.05, 0.1]
    }
    
    # Train with grid search
    grid_search = GridSearchCV(ensemble, param_grid, cv=3, scoring='neg_mean_squared_error')
    grid_search.fit(X_train, y_train)
    
    # Evaluate
    best_model = grid_search.best_estimator_
    y_pred = best_model.predict(X_test)
    
    print(f"Best Parameters: {grid_search.best_params_}")
    print(f"MSE: {mean_squared_error(y_test, y_pred):.4f}")
    print(f"R²: {r2_score(y_test, y_pred):.4f}")
    
    # Save model and feature importance
    joblib.dump(best_model, 'sfr_ensemble_model.joblib')
    feature_importance = pd.Series(best_model.named_estimators_['rf'].steps[1][1].feature_importances_,
                                   index=features)
    print("\nFeature Importance:")
    print(feature_importance.sort_values(ascending=False))

if __name__ == "__main__":
    main()
