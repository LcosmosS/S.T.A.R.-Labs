# Select the relevant columns (modify according to the actual column names)
target = 'log_SFR_Ha'  # Replace with your actual target column
features = ['log_Mass_gas', 'log_Mass', 'log_SFR_SF']  # Example features, adjust as needed


# Filter out rows with missing target or features
df_filtered = df[['CATAID', target] + features].dropna()


# Separate features (X) and target (y)
X = df_filtered[features]
y = df_filtered[target]


# Train a Random Forest model as an example
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score


# Split data into train and test
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)


# Initialize Random Forest Regressor
rf = RandomForestRegressor(random_state=42)


# Train the model
rf.fit(X_train, y_train)


# Make predictions
y_pred = rf.predict(X_test)


# Evaluate the model
mse = mean_squared_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)


# Print model performance
