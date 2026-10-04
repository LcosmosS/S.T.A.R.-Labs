# Initialize GridSearchCV with 5-fold cross-validation
grid_search = GridSearchCV(estimator=RandomForestRegressor(random_state=42),
                           param_grid=param_grid,
                           cv=5,
                           scoring='neg_mean_squared_error',
                           n_jobs=-1)  # Use all available cores


# Fit the grid search to the training data
grid_search.fit(X_train, y_train)


# Get the best hyperparameters
best_params = grid_search.best_params_
print(f"Best hyperparameters: {best_params}")
* Why: This step finds the combination of hyperparameters that minimizes the MSE across the training folds.
