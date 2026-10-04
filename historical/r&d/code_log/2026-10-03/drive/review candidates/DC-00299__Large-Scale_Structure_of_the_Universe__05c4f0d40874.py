    # Step 3: Create interaction term logmass * z
    # Ensure that 'logmass' is part of the dataframe and compute logmass if necessary
    if 'logmass' not in df1.columns:
        df1['logmass'] = np.log10(df1['mass'])  # Assuming 'mass' exists in the dataset
    
    df1['logmass_x_z'] = df1['logmass'] * df1['redshift']  # Interaction term


    # Step 4: Create feature set X and target y
    X = df1[['ra', 'dec', 'redshift', 'logmass', 'K', 'L', 'logmass_x_z']]  # Added interaction term
    y = df1['SFR']  # Target: 'SFR' (Star Formation Rate)
else:
    print("SFR column not available for target variable.")
    X = df1[['ra', 'dec', 'redshift', 'K', 'L']]  # Fallback if SFR is missing
    y = df1['SFR']  # Use SFR if available, otherwise fallback to a proxy or other method


# Step 5: Split data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)


# Step 6: Standardize the features (optional but often helpful for gradient-based models)
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)


# Step 7: Grid Search Hyperparameter Tuning for Random Forest
rf_param_grid = {
    'n_estimators': [100, 200, 500],
    'max_depth': [10, 20, 50, None],
    'min_samples_split': [2, 5, 10],
    'min_samples_leaf': [1, 2, 4],
    'max_features': ['sqrt', 'log2', None]
}


rf_grid_search = GridSearchCV(
    RandomForestRegressor(random_state=42),
    param_grid=rf_param_grid,
    cv=5,  # Cross-validation
    n_jobs=-1,  # Use all available cores
    scoring='r2'  # Optimize for R² score
)


rf_grid_search.fit(X_train_scaled, y_train)
best_rf_model = rf_grid_search.best_estimator_


# Step 8: Grid Search Hyperparameter Tuning for Gradient Boosting
gb_param_grid = {
    'n_estimators': [100, 200, 500],
    'learning_rate': [0.01, 0.1, 0.2],
    'max_depth': [3, 5, 10],
    'min_samples_split': [2, 5, 10],
    'min_samples_leaf': [1, 2, 4],
    'subsample': [0.7, 1.0]
}


gb_grid_search = GridSearchCV(
    GradientBoostingRegressor(random_state=42),
    param_grid=gb_param_grid,
    cv=5,  # Cross-validation
    n_jobs=-1,  # Use all available cores
    scoring='r2'  # Optimize for R² score
)


gb_grid_search.fit(X_train_scaled, y_train)
best_gb_model = gb_grid_search.best_estimator_


# Step 9: Evaluate both models' performance
# Random Forest Predictions
y_pred_rf = best_rf_model.predict(X_test_scaled)
mse_rf = mean_squared_error(y_test, y_pred_rf)
r2_rf = best_rf_model.score(X_test_scaled, y_test)


# Gradient Boosting Predictions
y_pred_gb = best_gb_model.predict(X_test_scaled)
mse_gb = mean_squared_error(y_test, y_pred_gb)
r2_gb = best_gb_model.score(X_test_scaled, y_test)
