from sklearn.model_selection import RandomizedSearchCV
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor


# Randomized search for Random Forest
rf_random_search = RandomizedSearchCV(
    RandomForestRegressor(random_state=42),
    param_distributions=rf_param_dist,
    n_iter=100,  # Number of different combinations to try
    cv=5,  # 5-fold cross-validation
    verbose=2,
    random_state=42,
    n_jobs=-1  # Use all cores
)


# Randomized search for Gradient Boosting
gb_random_search = RandomizedSearchCV(
    GradientBoostingRegressor(random_state=42),
    param_distributions=gb_param_dist,
    n_iter=100,  # Number of different combinations to try
    cv=5,  # 5-fold cross-validation
    verbose=2,
    random_state=42,
    n_jobs=-1  # Use all cores
)


# Fit the RandomizedSearchCV models
rf_random_search.fit(X_train, y_train)
gb_random_search.fit(X_train, y_train)


# Get the best models
best_rf_model = rf_random_search.best_estimator_
best_gb_model = gb_random_search.best_estimator_


print(f"Best Random Forest Model: {best_rf_model}")
print(f"Best Gradient Boosting Model: {best_gb_model}")
