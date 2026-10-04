print(f"Found flux columns: {flux_columns}")


# If we find any flux columns, we can use the first one found for SFR calculation
if flux_columns:
    flux_col = flux_columns[0]  # Take the first one found
    df1['SFR'] = df1[flux_col] / (1.26e-41)  # SFR in solar masses per year
    print(f"SFR column successfully created from {flux_col}.")
else:
    print("No 'fS' column found. Cannot calculate SFR.")


# --- Check for necessary columns and handle suffixes ---
if 'RAJ2000' in df1.columns:
    df1.rename(columns={'RAJ2000': 'ra'}, inplace=True)
if 'DEJ2000' in df1.columns:
    df1.rename(columns={'DEJ2000': 'dec'}, inplace=True)
if 'z' in df1.columns:
    df1.rename(columns={'z': 'redshift'}, inplace=True)


# After renaming, check if the required columns are available
print(f"Columns after renaming: {df1.columns}")


# Ensure 'SFR' is available as the target (we just calculated it above)
if 'SFR' in df1.columns:
    # Step 2: Impute missing values with the mean or median
    imputer = SimpleImputer(strategy='mean')  # You can change to 'median' if desired
    
    # Impute missing values in all numerical columns
    df1[['ra', 'dec', 'redshift', 'SFR']] = imputer.fit_transform(df1[['ra', 'dec', 'redshift', 'SFR']])


    X = df1[['ra', 'dec', 'redshift']]  # Use available features: ra, dec, and redshift
    y = df1['SFR']  # Target: 'SFR' (Star Formation Rate)
else:
    print("SFR column not available for target variable.")
    X = df1[['ra', 'dec', 'redshift']]  # Use available features if SFR is missing
    y = df1['SFR']  # Use SFR if available, otherwise fallback to a proxy or other method


# --- Polynomial Curve Fitting ---
# Fit a polynomial of degree 3 to the 'ra' feature (for simplicity)
degree = 3
polynomial_coefficients = np.polyfit(df1['ra'], df1['SFR'], degree)  # Fitting to 'ra' feature for simplicity


# Create a polynomial function from the coefficients
poly_func = np.poly1d(polynomial_coefficients)


# Calculate the polynomial fit and its derivative
df1['polynomial_fit'] = poly_func(df1['ra'])  # Polynomial fit for 'ra'
df1['polynomial_derivative'] = poly_func.deriv()(df1['ra'])  # Derivative of the polynomial for 'ra'


# --- Add the Polynomial Fit and Derivative as Features ---
X = df1[['ra', 'dec', 'redshift', 'polynomial_fit', 'polynomial_derivative']]  # Add new features


# Step 5: Split data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)


# Step 6: Standardize the features (optional but often helpful for gradient-based models)
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
best_rf_model = rf_random_search.best_estimator_


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
best_gb_model = gb_random_search.best_estimator_


# Step 9: Evaluate both models' performance
y_pred_rf = best_rf_model.predict(X_test_scaled)
mse_rf = mean_squared_error(y_test, y_pred_rf)
r2_rf = best_rf_model.score(X_test_scaled, y_test)


y_pred_gb = best_gb_model.predict(X_test_scaled)
mse_gb = mean_squared_error(y_test, y_pred_gb)
r2_gb = best_gb_model.score(X_test_scaled, y_test)
