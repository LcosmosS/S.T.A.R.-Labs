# --- Feature Selection ---
# Selecting features for modeling; this is just an example. You can refine which features are included.
X = df[['ra', 'dec', 'redshift', 'SFR_0_1Gyr_best_fit', 'mass_stellar_best_fit']]  # Select relevant features
y = df['SFR_0_1Gyr_best_fit']  # Target variable: Assuming this is a prediction target for SFR


# Step 2: Split data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)


# Step 3: Standardize the features (important for gradient-based models like Gradient Boosting)
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)


# --- Train the Random Forest Model using Randomized Search ---
rf_param_dist = {
    'n_estimators': randint(100, 1000),
    'max_depth': randint(10, 100),
    'min_samples_split': randint(2, 20),
    'min_samples_leaf': randint(1, 20),
    'max_features': ['sqrt', 'log2', None]  # Replaced 'auto' with 'sqrt' and 'log2'
}


rf_random_search = RandomizedSearchCV(
    RandomForestRegressor(random_state=42),
    param_distributions=rf_param_dist,
    n_iter=10,  # Number of random combinations to try
    cv=3,  # Cross-validation
    random_state=42,
    n_jobs=-1  # Use all available cores
)


rf_random_search.fit(X_train_scaled, y_train)
best_rf_random_model = rf_random_search.best_estimator_


# --- Grid Search to Fine-Tune the Best Parameters from RandomizedSearchCV ---
rf_param_grid = {
    'n_estimators': [best_rf_random_model.n_estimators - 50, best_rf_random_model.n_estimators, best_rf_random_model.n_estimators + 50],
    'max_depth': [best_rf_random_model.max_depth - 10, best_rf_random_model.max_depth, best_rf_random_model.max_depth + 10],
    'min_samples_split': [best_rf_random_model.min_samples_split - 2, best_rf_random_model.min_samples_split, best_rf_random_model.min_samples_split + 2],
    'min_samples_leaf': [best_rf_random_model.min_samples_leaf - 1, best_rf_random_model.min_samples_leaf, best_rf_random_model.min_samples_leaf + 1],
    'max_features': ['sqrt', 'log2']
}


rf_grid_search = GridSearchCV(
    RandomForestRegressor(random_state=42),
    param_grid=rf_param_grid,
    cv=3,
    n_jobs=-1
)


rf_grid_search.fit(X_train_scaled, y_train)
best_rf_model = rf_grid_search.best_estimator_


# --- Train the Gradient Boosting Model using Randomized Search ---
gb_param_dist = {
    'n_estimators': randint(100, 1000),
    'learning_rate': [0.001, 0.01, 0.1, 0.2, 0.3],
    'max_depth': randint(3, 20),
    'min_samples_split': randint(2, 20),
    'min_samples_leaf': randint(1, 20),
}


gb_random_search = RandomizedSearchCV(
    GradientBoostingRegressor(random_state=42),
    param_distributions=gb_param_dist,
    n_iter=10,  # Number of random combinations to try
    cv=3,  # Cross-validation
    random_state=42,
    n_jobs=-1  # Use all available cores
)


gb_random_search.fit(X_train_scaled, y_train)
best_gb_random_model = gb_random_search.best_estimator_


# --- Grid Search to Fine-Tune the Best Parameters from RandomizedSearchCV ---
gb_param_grid = {
    'n_estimators': [best_gb_random_model.n_estimators - 50, best_gb_random_model.n_estimators, best_gb_random_model.n_estimators + 50],
    'learning_rate': [best_gb_random_model.learning_rate - 0.01, best_gb_random_model.learning_rate, best_gb_random_model.learning_rate + 0.01],
    'max_depth': [best_gb_random_model.max_depth - 2, best_gb_random_model.max_depth, best_gb_random_model.max_depth + 2],
    'min_samples_split': [best_gb_random_model.min_samples_split - 1, best_gb_random_model.min_samples_split, best_gb_random_model.min_samples_split + 1],
    'min_samples_leaf': [best_gb_random_model.min_samples_leaf - 1, best_gb_random_model.min_samples_leaf, best_gb_random_model.min_samples_leaf + 1],
}


gb_grid_search = GridSearchCV(
    GradientBoostingRegressor(random_state=42),
    param_grid=gb_param_grid,
    cv=3,
    n_jobs=-1
)


gb_grid_search.fit(X_train_scaled, y_train)
best_gb_model = gb_grid_search.best_estimator_


# Step 4: Evaluate both models' performance
y_pred_rf = best_rf_model.predict(X_test_scaled)
mse_rf = mean_squared_error(y_test, y_pred_rf)
r2_rf = best_rf_model.score(X_test_scaled, y_test)


y_pred_gb = best_gb_model.predict(X_test_scaled)
mse_gb = mean_squared_error(y_test, y_pred_gb)
r2_gb = best_gb_model.score(X_test_scaled, y_test)
