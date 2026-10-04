    if model_type == 'linear':
        return LinearRegression()
    elif model_type == 'random_forest':
        return RandomForestRegressor(n_estimators=100, random_state=42)
    elif model_type == 'gradient_boosting':
        return GradientBoostingRegressor(n_estimators=100, random_state=42)
    else:
        raise ValueError("Invalid model type. Choose 'linear', 'random_forest', or 'gradient_boosting'.")


def create_features(df, high_mass_threshold, low_mass_threshold, additional_features):
    """
    Generate feature matrix with non-linear terms and mass-specific adjustments.
