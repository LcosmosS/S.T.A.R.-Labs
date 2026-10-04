from sklearn.model_selection import RandomizedSearchCV, GridSearchCV
from sklearn.ensemble import RandomForestRegressor
from scipy.stats import randint


# Step 1: Use RandomizedSearchCV for a broad search
rf_param_dist = {
    'n_estimators': randint(100, 1000),
    'max_depth': randint(10, 100),
    'min_samples_split': randint(2, 20),
    'min_samples_leaf': randint(1, 20),
    'max_features': ['sqrt', 'log2', None]  # Use broad choices for initial search
}


rf_random_search = RandomizedSearchCV(
    RandomForestRegressor(),
    param_distributions=rf_param_dist,
    n_iter=100,  # Number of random combinations to try
    cv=3,
    random_state=42,
    n_jobs=-1
)


rf_random_search.fit(X_train, y_train)
best_params_random = rf_random_search.best_params_
print(f"Best parameters from RandomizedSearchCV: {best_params_random}")


# Step 2: Use GridSearchCV for a finer search based on the random search results
rf_param_grid = {
    'n_estimators': [best_params_random['n_estimators'] - 50, best_params_random['n_estimators'], best_params_random['n_estimators'] + 50],
    'max_depth': [best_params_random['max_depth'] - 10, best_params_random['max_depth'], best_params_random['max_depth'] + 10],
    'min_samples_split': [best_params_random['min_samples_split'] - 2, best_params_random['min_samples_split'], best_params_random['min_samples_split'] + 2],
    'min_samples_leaf': [best_params_random['min_samples_leaf'] - 1, best_params_random['min_samples_leaf'], best_params_random['min_samples_leaf'] + 1],
    'max_features': ['sqrt', 'log2']
}


rf_grid_search = GridSearchCV(
    RandomForestRegressor(),
    param_grid=rf_param_grid,
    cv=3,
    n_jobs=-1
)


rf_grid_search.fit(X_train, y_train)
best_params_grid = rf_grid_search.best_params_
print(f"Best parameters from GridSearchCV: {best_params_grid}")


# Step 3: Train model with best parameters from GridSearchCV
best_rf_model = rf_grid_search.best_estimator_
