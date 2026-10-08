import pandas as pd
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.ensemble import GradientBoostingRegressor, RandomForestRegressor
from sklearn.metrics import mean_squared_error, r2_score
import matplotlib.pyplot as plt

# --- Load Dataset ---
print("Loading datasets...")
pipe3d_data_path = 'pipe3d_data.csv'  # Path inside WSL
df_main = pd.read_csv(pipe3d_data_path)

# --- Inspect the Columns ---
print("Columns in pipe3d dataset:", df_main.columns)

# --- Define Features and Target ---
# Based on available columns, let's assume these are the columns we want to use
features = [
    'log_Mass_gas',        # Assuming this column is in your dataset
    'log_SFR_SF',          # Assuming this column is in your dataset
    'log_SFR_D_C',         # Assuming this column is in your dataset
    'OH_O3N2_cen'          # Assuming this column is in your dataset
]
target = 'log_SFR_Ha'  # The target variable

# --- Clean Data ---
# Ensure that the 'CATAID' or appropriate identifier column is present
identifier_column = 'mangaid'  # If 'CATAID' is not in the dataset, using 'mangaid'

# Check if the target and features are present in the dataset
df_clean = df_main[[identifier_column] + features + [target]].dropna()

# Extract features (X) and target (y)
X = df_clean[features]
y = df_clean[target]

# --- Split Data into Training and Testing Sets ---
print("Splitting data into training and testing sets...")
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# --- Train Gradient Boosting Model ---
print("Training Gradient Boosting model...")
gb = GradientBoostingRegressor(random_state=42)
gb.fit(X_train, y_train)

# --- Train Random Forest Model ---
print("Training Random Forest model...")
rf = RandomForestRegressor(random_state=42)
rf.fit(X_train, y_train)

# --- Make Predictions ---
y_pred_gb = gb.predict(X_test)
y_pred_rf = rf.predict(X_test)

# --- Evaluate Models on Test Set ---
mse_gb = mean_squared_error(y_test, y_pred_gb)
r2_gb = r2_score(y_test, y_pred_gb)
mse_rf = mean_squared_error(y_test, y_pred_rf)
r2_rf = r2_score(y_test, y_pred_rf)

print("\nModel Performance on Test Set:")
print(f"Gradient Boosting - MSE: {mse_gb:.4f}, R²: {r2_gb:.4f}")
print(f"Random Forest - MSE: {mse_rf:.4f}, R²: {r2_rf:.4f}")

# --- Perform 5-Fold Cross-Validation ---
print("\nPerforming 5-fold cross-validation...")
cv_mse_gb = -cross_val_score(gb, X, y, cv=5, scoring='neg_mean_squared_error').mean()
cv_r2_gb = cross_val_score(gb, X, y, cv=5, scoring='r2').mean()
cv_mse_rf = -cross_val_score(rf, X, y, cv=5, scoring='neg_mean_squared_error').mean()
cv_r2_rf = cross_val_score(rf, X, y, cv=5, scoring='r2').mean()

print(f"Cross-Validation MSE (Gradient Boosting): {cv_mse_gb:.4f}, R²: {cv_r2_gb:.4f}")
print(f"Cross-Validation MSE (Random Forest): {cv_mse_rf:.4f}, R²: {cv_r2_rf:.4f}")

# --- Visualize Results ---
# Residual Plot for Random Forest
plt.figure(figsize=(8, 6))
residuals_rf = y_test - y_pred_rf
plt.scatter(y_pred_rf, residuals_rf, alpha=0.5)
plt.axhline(0, color='red', linestyle='--')
plt.xlabel('Predicted SFR')
plt.ylabel('Residuals')
plt.title('Residuals vs Predicted SFR (Random Forest)')
plt.show()

# Feature Importance for Random Forest
plt.figure(figsize=(8, 6))
importances = rf.feature_importances_
feature_names = X.columns
sorted_idx = importances.argsort()
plt.barh(feature_names[sorted_idx], importances[sorted_idx])
plt.xlabel('Importance')
plt.title('Feature Importances (Random Forest)')
plt.show()
