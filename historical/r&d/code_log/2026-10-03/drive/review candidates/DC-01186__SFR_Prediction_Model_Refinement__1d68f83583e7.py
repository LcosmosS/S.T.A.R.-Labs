import pandas as pd
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.ensemble import GradientBoostingRegressor, RandomForestRegressor
from sklearn.metrics import mean_squared_error, r2_score
import matplotlib.pyplot as plt


# --- Load Datasets ---
print("Loading datasets...")


# Load the filtered dataset
df_main = pd.read_csv('/home/pmqr7/path/to/your/pipe3d_data.csv')  # Ensure to use the correct path for your file
df_class = pd.read_csv('/home/pmqr7/path/to/your/GalaxiesClassified.csv')
df_stellar = pd.read_csv('/home/pmqr7/path/to/your/Stellar_Mass2_Table.csv')
df_environment = pd.read_csv('/home/pmqr7/path/to/your/EnvironmentMeasures.csv')


# --- Feature and Target Selection ---
features = [
    'log_Mass', 'log_SFR_ssp', 'log_NII_Ha_cen', 'log_OIII_Hb_cen', 'log_SII_Ha_cen', 'log_OII_Hb_cen',
    'log_Mass_gas', 'vel_sigma_Re', 'log_SFR_SF', 'OH_O3N2_cen', 'OH_N2_cen', 'OH_ONS_cen', 'OH_R23_cen'
]
target = 'SFR_0_1Gyr_best_fit'


# --- Filter Datasets (avoiding merging) ---
print("Filtering datasets...")


# Selecting only the necessary columns and filtering the data
df_main = df_main[['CATAID'] + features + [target]].dropna()
df_class = df_class[['CATAID']]  # Adjust if you need specific columns
df_stellar = df_stellar[['CATAID', 'logmstar']]  # Adjust to the relevant columns from Stellar dataset
df_environment = df_environment[['CATAID', 'DistanceTo5nn']]  # Adjust to the relevant columns from Environment dataset


# Merge these filtered datasets based on 'CATAID' (if needed, for analysis)
df_combined = df_main.merge(df_class, on='CATAID', how='left')
df_combined = df_combined.merge(df_stellar, on='CATAID', how='left')
df_combined = df_combined.merge(df_environment, on='CATAID', how='left')


print(f"Filtered dataset size: {df_combined.shape[0]} rows")


# --- Extract Features and Target ---
X = df_combined[features]
y = df_combined[target]


# --- Split Data into Training and Testing Sets ---
print("Splitting data into training and testing sets...")
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)


# --- Train Models ---
print("Training Gradient Boosting model...")
gb = GradientBoostingRegressor(random_state=42)
gb.fit(X_train, y_train)


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
