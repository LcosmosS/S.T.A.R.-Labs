from sklearn.model_selection import GridSearchCV


# Define the parameter grid
param_grid = {
    'n_estimators': [100, 200, 300],
    'max_depth': [10, 20, None],
    'min_samples_split': [2, 5, 10]
}


# Initialize Grid Search with cross-validation
grid_search = GridSearchCV(estimator=RandomForestRegressor(random_state=42), param_grid=param_grid, cv=5, scoring='neg_mean_squared_error')
grid_search.fit(X_train, y_train)


# Get the best model
best_rf_model = grid_search.best_estimator_


# Evaluate the tuned model
y_pred_tuned = best_rf_model.predict(X_test)
mse_tuned = mean_squared_error(y_test, y_pred_tuned)
r2_tuned = r2_score(y_test, y_pred_tuned)
print(f"Tuned MSE: {mse_tuned:.4f}")
print(f"Tuned R-squared: {r2_tuned:.4f}")
* Why it matters: Tuning hyperparameters can significantly improve model performance by finding the optimal balance between bias and variance.
