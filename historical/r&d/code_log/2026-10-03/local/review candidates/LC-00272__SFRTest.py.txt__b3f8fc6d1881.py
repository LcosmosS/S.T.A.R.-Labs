import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import GradientBoostingRegressor, RandomForestRegressor
from sklearn.metrics import mean_squared_error, r2_score
import matplotlib.pyplot as plt

# --- Correct Data Path ---
pipe3d_data_path = '/mnt/data/pipe3d_data.csv'  # Correct path to your pipe3d_data.csv file

# --- Load Dataset ---
print("Loading dataset...")
df_main = pd.read_csv(pipe3d_data_path)

# --- Focused Feature Selection ---
# Selecting only the relevant features and target
features = ['log_Mass_gas', 'log_SFR_Ha', 'log_Mass', 'log_SFR_ssp', 'mass_stellar_best_fit']
target = 'SFR_0_1Gyr_best_fit'

# --- Data Filtering: Remove rows with missing values in important columns ---
df_clean = df_main[['CATAID'] + features + [target]].dropna()

# --- Split Data for Training and Testing ---
X = df_clean[features]
y = df_clean[target]
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# --- Model Training ---
print("Training models...")

# Gradient Boosting Regressor
gb = GradientBoostingRegressor(random_state=42)
gb.fit(X_train, y_train)

# Random Forest Regressor
rf = RandomForestRegressor(random_state=42)
rf.fit(X_train, y_train)

# --- Predictions ---
y_pred_gb = gb.predict(X_test)
y_pred_rf = rf.predict(X_test)

# --- Model Evaluation ---
mse_gb = mean_squared_error(y_test, y_pred_gb)
r2_gb = r2_score(y_test, y_pred_gb)
mse_rf = mean_squared_error(y_test, y_pred_rf)
r2_rf = r2_score(y_test, y_pred_rf)

# Print performance metrics
print(f"Gradient Boosting - MSE: {mse_gb:.4f}, R²: {r2_gb:.4f}")
print(f"Random Forest - MSE: {mse_rf:.4f}, R²: {r2_rf:.4f}")

# --- Visualizations ---
# Residual Plot for Gradient Boosting
plt.figure(figsize=(8, 6))
residuals_gb = y_test - y_pred_gb
plt.scatter(y_pred_gb, residuals_gb, alpha=0.5)
plt.axhline(0, color='red', linestyle='--')
plt.xlabel('Predicted SFR')
plt.ylabel('Residuals')
plt.title('Residuals vs Predicted SFR (Gradient Boosting)')
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
