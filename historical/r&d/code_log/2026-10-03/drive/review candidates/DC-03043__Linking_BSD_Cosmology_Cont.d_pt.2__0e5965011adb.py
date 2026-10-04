from sklearn.model_selection import GridSearchCV
# Define the hyperparameter grid
param_grid = { 'n_estimators': [100, 200, 300], 'max_depth': [10, 20, 30, None], 'min_samples_split': [2, 5, 10], 'min_samples_leaf': [1, 2, 4] }
# Initialize GridSearchCV
grid_search = GridSearchCV(estimator=rf_model, param_grid=param_grid, cv=5, scoring='neg_mean_squared_error', n_jobs=-1)
# Fit the grid search to the training data
grid_search.fit(X_train, y_train)
# Get the best hyperparameters
best_params = grid_search.best_params_ print(f"Best hyperparameters: {best_params}")
