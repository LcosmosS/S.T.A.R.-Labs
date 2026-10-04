def get_model(model_type):
    if model_type == 'linear':
        return LinearRegression()
    elif model_type == 'random_forest':
        return RandomForestRegressor(n_estimators=100, random_state=42)
    elif model_type == 'gradient_boosting':
        return GradientBoostingRegressor(n_estimators=100, random_state=42)
    else:
        raise ValueError("Invalid model type")
