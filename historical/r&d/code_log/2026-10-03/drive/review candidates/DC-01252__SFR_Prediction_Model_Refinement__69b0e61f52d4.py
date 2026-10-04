print(f"Found flux columns: {flux_columns}")


# If we find any flux columns, we can use the first one found for SFR calculation
if flux_columns:
    flux_col = flux_columns[0]  # Take the first one found
    df1['SFR'] = df1[flux_col] / (1.26e-41)  # SFR in solar masses per year
    print(f"SFR column successfully created from {flux_col}.")
else:
    print("No 'fS' column found. Cannot calculate SFR.")
    # Skip calculation and handle this case if needed


# --- Check for necessary columns and handle suffixes ---
# Rename RAJ2000 to ra, DEJ2000 to dec, and z to redshift
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
    # Drop rows with NaN in 'SFR'
    df1 = df1.dropna(subset=['SFR'])
    X = df1[['ra', 'dec', 'redshift']]  # Use available features: ra, dec, and redshift
    y = df1['SFR']  # Target: 'SFR' (Star Formation Rate)
else:
    print("SFR column not available for target variable.")
    X = df1[['ra', 'dec', 'redshift']]  # Use available features if SFR is missing
    y = df1['SFR']  # Use SFR if available, otherwise fallback to a proxy or other method


# Step 5: Split data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)


# Step 6: Standardize the features (optional but often helpful for gradient-based models)
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)


# Step 7: Train the model using Random Forest Regressor
model = RandomForestRegressor(n_estimators=100, random_state=42)
model.fit(X_train_scaled, y_train)


# Step 8: Predict on the test set
y_pred = model.predict(X_test_scaled)


# Step 9: Evaluate the model's performance
mse = mean_squared_error(y_test, y_pred)
r2 = model.score(X_test_scaled, y_test)
