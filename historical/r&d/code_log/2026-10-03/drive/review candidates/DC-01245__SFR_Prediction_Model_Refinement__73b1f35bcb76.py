if missing_columns:
    print(f"Missing columns: {missing_columns}")
    # You can create or rename columns here, for example:
    df1.rename(columns={'log_Mass_x': 'log_Mass', 'log_Mass_y': 'log_Mass'}, inplace=True)
    df1.rename(columns={'ra_x': 'ra', 'ra_y': 'ra'}, inplace=True)


# --- Randomly select features ---
np.random.seed(42)
X = df1[['log_Mass', 'sfr', 'redshift', 'metallicity', 'ra', 'dec']]  # Example feature columns
y = df1['sfr']  # Target: 'sfr' (Star Formation Rate)


# Step 5: Split data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)


# Step 6: Standardize the features
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
