from sklearn.model_selection import GridSearchCV


# Random Forest
rf_params = {'n_estimators': [100, 200], 'max_depth': [10, 20, None]}
rf_grid = GridSearchCV(RandomForestRegressor(random_state=42), rf_params, cv=5)
rf_grid.fit(X_train, y_train)
print("Best RF params:", rf_grid.best_params_)


# Gradient Boosting
gb_params = {'n_estimators': [100, 200], 'learning_rate': [0.01, 0.1], 'max_depth': [3, 5]}
gb_grid = GridSearchCV(GradientBoostingRegressor(random_state=42), gb_params, cv=5)
gb_grid.fit(X_train, y_train)
* print("Best GB params:", gb_grid.best_params_)
