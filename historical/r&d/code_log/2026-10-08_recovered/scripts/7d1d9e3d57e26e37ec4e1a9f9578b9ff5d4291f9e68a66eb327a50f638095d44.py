import pandas as pd
import numpy as np
import shap
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.ensemble import GradientBoostingRegressor, RandomForestRegressor
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.model_selection import cross_val_score

# --- Load Dataset ---
print("Loading dataset...")
sdss_data_path = 'SDSSDR18_200000.csv'  # Update with the correct path
df_main = pd.read_csv(sdss_data_path)

# --- Randomly select features ---
np.random.seed(42)
features = np.random.choice(df_main.columns, size=5, replace=False).tolist()
target = 'logmstar'  # Target column

# --- Extract Features (X) and Target (y) ---
X = df_main[features]
y = df_main[target]

# --- Split Data into Training and Testing Sets ---
print("Splitting data into training and testing sets...")
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
print(f"Training set size: {X_train.shape[0]} rows")
print(f"Test set size: {X_test.shape[0]} rows")

# --- Train Gradient Boosting Model ---
print("Training Gradient Boosting model...")
gb = GradientBoostingRegressor(random_state=42)
gb.fit(X_train, y_train)

# --- Train Random Forest Model ---
print("Training Random Forest model...")
rf = RandomForestRegressor(random_state=42)
rf.fit(X_train, y_train)

# --- Evaluate Models ---
y_pred_gb = gb.predict(X_test)
y_pred_rf = rf.predict(X_test)

# --- Calculate MSE and R² ---
mse_gb = mean_squared_error(y_test, y_pred_gb)
r2_gb = r2_score(y_test, y_pred_gb)

mse_rf = mean_squared_error(y_test, y_pred_rf)
r2_rf = r2_score(y_test, y_pred_rf)

# --- Print Model Performance ---
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

# --- SHAP Value Calculation for Gradient Boosting ---
print("\nCalculating SHAP values for Gradient Boosting model...")
explainer_gb = shap.TreeExplainer(gb)
shap_values_gb = explainer_gb.shap_values(X_test)

# --- SHAP Summary Plot for Gradient Boosting ---
print("\nPlotting SHAP summary plot for Gradient Boosting model...")
shap.summary_plot(shap_values_gb, X_test)

# --- SHAP Value Calculation for Random Forest ---
print("\nCalculating SHAP values for Random Forest model...")
explainer_rf = shap.TreeExplainer(rf)
shap_values_rf = explainer_rf.shap_values(X_test)

# --- SHAP Summary Plot for Random Forest ---
print("\nPlotting SHAP summary plot for Random Forest model...")
shap.summary_plot(shap_values_rf, X_test)

# --- Save Plots ---
print("\nSaving SHAP plots...")
plt.savefig('shap_gb_summary_plot.png')  # Save the Gradient Boosting SHAP plot
plt.savefig('shap_rf_summary_plot.png')  # Save the Random Forest SHAP plot
