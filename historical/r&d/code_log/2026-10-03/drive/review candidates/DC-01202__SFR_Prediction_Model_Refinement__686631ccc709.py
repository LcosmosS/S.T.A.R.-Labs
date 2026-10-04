import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import GradientBoostingRegressor, RandomForestRegressor
from sklearn.metrics import mean_squared_error, r2_score


# Load dataset
sdss_data_path = '/path/to/your/SDSSDR18_200000.csv'  # Ensure this is the correct path
df_main = pd.read_csv(sdss_data_path)


# Columns to use for feature selection (adjust based on your preference)
features = ['ra', 'dec', 'u', 'g', 'r', 'i', 'z', 'redshift']  # Example, modify as needed
target = 'redshift'  # Example, modify if you want a different target


# Extract features (X) and target (y)
X = df_main[features]
y = df_main[target]


# Split data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)


# Train Gradient Boosting model
print("Training Gradient Boosting model...")
gb = GradientBoostingRegressor(random_state=42)
gb.fit(X_train, y_train)


# Train Random Forest model
print("Training Random Forest model...")
rf = RandomForestRegressor(random_state=42)
rf.fit(X_train, y_train)


# Evaluate the models
y_pred_gb = gb.predict(X_test)
y_pred_rf = rf.predict(X_test)


# Calculate MSE and R^2
mse_gb = mean_squared_error(y_test, y_pred_gb)
r2_gb = r2_score(y_test, y_pred_gb)


mse_rf = mean_squared_error(y_test, y_pred_rf)
r2_rf = r2_score(y_test, y_pred_rf)


# Print model performance
print("\nModel Performance on Test Set:")
print(f"Gradient Boosting - MSE: {mse_gb:.4f}, R²: {r2_gb:.4f}")
print(f"Random Forest - MSE: {mse_rf:.4f}, R²: {r2_rf:.4f}")
