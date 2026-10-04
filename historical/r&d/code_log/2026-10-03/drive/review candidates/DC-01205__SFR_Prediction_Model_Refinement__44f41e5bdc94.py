import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.metrics import mean_squared_error, r2_score


# --- Load the Dataset ---
print("Loading dataset...")
file_path = '/path/to/your/SDSSDR18_200000.csv'
df = pd.read_csv(file_path)


# --- Define Features and Target ---
# Targeting four features (adjust based on your actual goal)
features = ['ra', 'dec', 'u', 'g']  # Replace with your chosen features
target = 'redshift'  # The target variable you're predicting, adjust as needed


# --- Clean Data ---
print("Cleaning data...")
df_clean = df[features + [target]].dropna()
print(f"Dataset size after cleaning: {df_clean.shape[0]} rows")


# Extract features (X) and target (y)
X = df_clean[features]
y = df_clean[target]


# --- Split Data into Training and Testing Sets ---
print("Splitting data into training and testing sets...")
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)


# Print the first 5 rows of the training and testing sets
print("\nFirst 5 rows of the training set (X_train):")
print(X_train.head())


print("\nFirst 5 rows of the testing set (X_test):")
print(X_test.head())


print("\nFirst 5 rows of the target training set (y_train):")
print(y_train.head())


print("\nFirst 5 rows of the target testing set (y_test):")
print(y_test.head())


# --- Train the Model ---
print("Training Gradient Boosting model...")
gb = GradientBoostingRegressor(random_state=42)
gb.fit(X_train, y_train)


# --- Make Predictions ---
y_pred_gb = gb.predict(X_test)


# --- Evaluate the Model ---
mse_gb = mean_squared_error(y_test, y_pred_gb)
r2_gb = r2_score(y_test, y_pred_gb)


print("\nModel Performance on Test Set:")
print(f"Gradient Boosting - MSE: {mse_gb:.4f}, R²: {r2_gb:.4f}")
