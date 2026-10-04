# Step 4: Feature Engineering
# Calculate color indices as additional features
df['u_g'] = df['u'] - df['g']
df['g_r'] = df['g'] - df['r']
df['r_i'] = df['r'] - df['i']
df['i_z'] = df['i'] - df['z']


# Select features and target variable
X = df[['ra', 'dec', 'redshift', 'u_g', 'g_r', 'r_i', 'i_z']]
y = df['redshift']  # Assuming we want to predict redshift; adjust as needed


# Step 5: Split data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)


# Step 6: Standardize the features
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)


# Step 7: Initialize models
rf_model = RandomForestRegressor(random_state=42)
gb_model = GradientBoostingRegressor(random_state=42)


# Step 8: Define hyperparameter grids for RandomizedSearchCV and GridSearchCV


# Randomized Search Hyperparameter Grid
rf_param_dist = {
    'n_estimators': randint(100, 300),
    'max_depth': randint(10, 30),
    'min_samples_split': randint(2, 10),
    'min_samples_leaf': randint(1, 4),
    'max_features': ['sqrt', 'log2', None]
}


gb_param_dist = {
    'n_estimators': randint(100, 300),
    'learning_rate': uniform(0.01, 0.3),
    'max_depth': randint(3, 7),
    'min_samples_split': randint(2, 10),
    'min_samples_leaf': randint(1, 4)
}


# Grid Search Hyperparameter Grid (fine-tuning after RandomizedSearchCV)
rf_param_grid = {
    'n_estimators': [200, 250],
    'max_depth': [20, 25],
    'min_samples_split': [2, 5],
    'min_samples_leaf': [1, 2],
    'max_features': ['sqrt', 'log2']
}


gb_param_grid = {
    'n_estimators': [200, 250],
    'learning_rate': [0.05, 0.1],
    'max_depth': [5, 7],
    'min_samples_split': [2, 5],
    'min_samples_leaf': [1, 2]
}


# Step 9: Perform RandomizedSearchCV to get a rough idea of the best hyperparameters
rf_random_search = RandomizedSearchCV(estimator=rf_model, param_distributions=rf_param_dist, n_iter=10, cv=3, n_jobs=-1, verbose=2, random_state=42)
gb_random_search = RandomizedSearchCV(estimator=gb_model, param_distributions=gb_param_dist, n_iter=10, cv=3, n_jobs=-1, verbose=2, random_state=42)


# Fit the models using RandomizedSearchCV
print("Starting RandomizedSearchCV for RandomForest...")
rf_random_search.fit(X_train_scaled, y_train)


print("Starting RandomizedSearchCV for GradientBoosting...")
gb_random_search.fit(X_train_scaled, y_train)


# Step 10: Use GridSearchCV for fine-tuning based on best parameters from RandomizedSearchCV
print("Starting GridSearchCV for RandomForest...")
rf_best_params = rf_random_search.best_params_  # Get best params from RandomizedSearchCV
rf_grid_search = GridSearchCV(estimator=rf_model, param_grid=rf_param_grid, cv=3, n_jobs=-1, verbose=2)
rf_grid_search.fit(X_train_scaled, y_train)


print("Starting GridSearchCV for GradientBoosting...")
gb_best_params = gb_random_search.best_params_  # Get best params from RandomizedSearchCV
gb_grid_search = GridSearchCV(estimator=gb_model, param_grid=gb_param_grid, cv=3, n_jobs=-1, verbose=2)
gb_grid_search.fit(X_train_scaled, y_train)


# Step 11: Evaluate the models
rf_best_model = rf_grid_search.best_estimator_
gb_best_model = gb_grid_search.best_estimator_


# Predict on the test set
y_pred_rf = rf_best_model.predict(X_test_scaled)
y_pred_gb = gb_best_model.predict(X_test_scaled)


# Calculate performance metrics
mse_rf = mean_squared_error(y_test, y_pred_rf)
r2_rf = rf_best_model.score(X_test_scaled, y_test)


mse_gb = mean_squared_error(y_test, y_pred_gb)
r2_gb = gb_best_model.score(X_test_scaled, y_test)
