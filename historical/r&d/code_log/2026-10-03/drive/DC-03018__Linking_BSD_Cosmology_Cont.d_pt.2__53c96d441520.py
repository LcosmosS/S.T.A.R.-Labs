from sklearn.model_selection import RandomizedSearchCV from sklearn.ensemble import RandomForestRegressor
# Define the model
rf = RandomForestRegressor(random_state=42)
# Define the hyperparameter grid
param_dist = { 'n_estimators': [50, 100, 200], 'max_depth': [10, 20, None], 'min_samples_split': [2, 5, 10], 'min_samples_leaf': [1, 2, 4] }
# Set up RandomizedSearchCV
random_search = RandomizedSearchCV(estimator=rf, param_distributions=param_dist, n_iter=10, cv=5, scoring='neg_mean_squared_error', random_state=42, n_jobs=-1)
# Fit the model
random_search.fit(X_train, y_train)
# Get the best parameters
best_params = random_search.best_params_ print(f"Best hyperparameters: {best_params}")
