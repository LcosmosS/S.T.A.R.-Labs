from sklearn.model_selection import GridSearchCV


# Define parameter grid
param_grid = {
    'n_estimators': [50, 100, 200],
    'max_depth': [10, 20, None],
    'min_samples_split': [2, 5, 10]
}


# Perform grid search within cross-validation
model = RandomForestRegressor(random_state=42)
grid_search = GridSearchCV(model, param_grid, cv=5, scoring='neg_mean_squared_error')
grid_search.fit(X, y)  # Fit on the full dataset initially
best_model = grid_search.best_estimator_
print(f"Best parameters: {grid_search.best_params_}")


# Use best_model for cross-validation
for fold, (train_idx, test_idx) in enumerate(kf.split(X)):
    X_train, X_test = X[train_idx], X[test_idx]
    y_train, y_test = y[train_idx], y[test_idx]
    best_model.fit(X_train, y_train)
    y_pred = best_model.predict(X_test)
    mse = mean_squared_error(y_test, y_pred)
    mse_list.append(mse)
*     print(f"Fold {fold+1} MSE: {mse:.4f}")
* Replace: In the original script, replace the model definition and cross-validation loop with this tuned approach.
