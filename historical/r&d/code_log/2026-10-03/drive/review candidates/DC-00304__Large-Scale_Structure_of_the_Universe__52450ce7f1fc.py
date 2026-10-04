from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import mean_squared_error


# Calculate the L-function (or its equivalent) for each row
# This step is based on your curve fitting, we assume it's stored in 'L_function' column
df1['L_function'] = poly(X['ra'])  # Assuming the curve fit returns an output for 'ra'


# Add the 'L_function' as a feature for prediction
X = df1[['ra', 'dec', 'redshift', 'L_function']]  # Include 'L_function' as an additional feature
y = df1['SFR']  # Target


# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)


# Standardize the features
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)


# Train a Random Forest model
rf_model = RandomForestRegressor(n_estimators=100, random_state=42)
rf_model.fit(X_train_scaled, y_train)


# Train a Gradient Boosting model
gb_model = GradientBoostingRegressor(n_estimators=100, learning_rate=0.1, random_state=42)
gb_model.fit(X_train_scaled, y_train)


# Predict and evaluate both models
y_pred_rf = rf_model.predict(X_test_scaled)
y_pred_gb = gb_model.predict(X_test_scaled)


# Evaluate performance using Mean Squared Error and R² score
mse_rf = mean_squared_error(y_test, y_pred_rf)
r2_rf = rf_model.score(X_test_scaled, y_test)


mse_gb = mean_squared_error(y_test, y_pred_gb)
r2_gb = gb_model.score(X_test_scaled, y_test)
