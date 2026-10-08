import pandas as pd
import numpy as np
from sklearn.ensemble import GradientBoostingRegressor, RandomForestRegressor
from sklearn.model_selection import train_test_split, RandomizedSearchCV
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt

# --- 1. Load All Datasets ---
print("Loading datasets...")
df_sfr = pd.read_csv('compiled_sfr_dataset.csv')
df_galaxies = pd.read_csv('GalaxiesClassified.csv')
df_stellar = pd.read_csv('StellarMassesLambdar.csv')
df_magphys = pd.read_csv('MagPhys.csv')
df_env = pd.read_csv('EnvironmentMeasures.csv')

# --- 2. Add Temporary Index for Merging ---
# Assign a temporary index to each dataset to facilitate merging without common columns
df_sfr['temp_index'] = range(len(df_sfr))
df_galaxies['temp_index'] = range(len(df_galaxies))
df_stellar['temp_index'] = range(len(df_stellar))
df_magphys['temp_index'] = range(len(df_magphys))
df_env['temp_index'] = range(len(df_env))

# --- 3. Merge Datasets ---
print("\nMerging all datasets regardless of matching column names...")
# First, merge datasets with 'CATAID' where available
df_with_cataid = (df_galaxies.merge(df_stellar, on=['CATAID', 'temp_index'], how='outer')
                  .merge(df_magphys, on=['CATAID', 'temp_index'], how='outer')
                  .merge(df_env, on=['CATAID', 'temp_index'], how='outer'))

# Then, concatenate with compiled_sfr_dataset.csv using the temporary index
df_combined = pd.concat([df_with_cataid, df_sfr], axis=1, ignore_index=False)

# Drop the temporary index column after merging
df_combined = df_combined.drop(columns=['temp_index'], errors='ignore')
print(f"Combined dataset size: {df_combined.shape}")
print("Columns in combined dataset:", df_combined.columns.tolist())

# --- 4. Define Target and Select Features ---
# Use 'SFR_0_1Gyr_percentile50' from MagPhys as the target if available, else adjust
target = 'SFR_0_1Gyr_percentile50'
if target not in df_combined.columns:
    print(f"Warning: '{target}' not found. Using 'log_SFR_Ha' from compiled_sfr_dataset.csv instead.")
    target = 'log_SFR_Ha'

# Select a subset of features for modeling (you can adjust this list as needed)
features = [
    'logmstar', 'mass_stellar_percentile50', 'mass_dust_percentile50',
    'metalicity_Z_Zo_percentile50', 'logage', 'logtau', 'extBV',
    'DistanceTo5nn', 'SurfaceDensity', 'GeoS4', 'GeoS10', 'log_SFR_Ha',
    'log_Mass_gas', 'log_SFR_sed'
]
# Filter features to only those present in the combined dataset
features = [f for f in features if f in df_combined.columns]
print(f"Selected features for modeling: {features}")

# --- 5. Preprocess Data ---
df_combined = df_combined.dropna(subset=[target] + features)
X = df_combined[features]
y = df_combined[target]
print(f"Rows after preprocessing: {X.shape[0]}")

scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# --- 6. Split Data ---
X_train, X_test, y_train, y_test = train_test_split(
    X_scaled, y, test_size=0.2, random_state=42
)
print(f"Training set size: {X_train.shape[0]}, Test set size: {X_test.shape[0]}")

# --- 7. Model Training ---
rf_params = {
    'n_estimators': [100, 200, 300],
    'max_depth': [10, 20, None],
    'min_samples_split': [2, 5, 10]
}
gb_params = {
    'learning_rate': [0.01, 0.05, 0.1],
    'max_depth': [3, 5, 7],
    'n_estimators': [100, 200, 300]
}

print("\nTuning Random Forest...")
rf_random = RandomizedSearchCV(
    RandomForestRegressor(random_state=42), rf_params, n_iter=10, cv=3,
    scoring='neg_mean_squared_error', n_jobs=-1, random_state=42
)
rf_random.fit(X_train, y_train)
best_rf = rf_random.best_estimator_
print(f"Best RF params: {rf_random.best_params_}")

print("Tuning Gradient Boosting...")
gb_random = RandomizedSearchCV(
    GradientBoostingRegressor(random_state=42, loss='huber'), gb_params,
    n_iter=10, cv=3, scoring='neg_mean_squared_error', n_jobs=-1, random_state=42
)
gb_random.fit(X_train, y_train)
best_gb = gb_random.best_estimator_
print(f"Best GB params: {gb_random.best_params_}")

# --- 8. Evaluate Models ---
def evaluate_model(model, X_test, y_test, name):
    y_pred = model.predict(X_test)
    mse = mean_squared_error(y_test, y_pred)
    r2 = r2_score(y_test, y_pred)
    print(f"\n{name} - MSE: {mse:.4f}, R²: {r2:.4f}")
    return y_pred

rf_pred = evaluate_model(best_rf, X_test, y_test, "Random Forest")
gb_pred = evaluate_model(best_gb, X_test, y_test, "Gradient Boosting")

# --- 9. Feature Importance ---
rf_importance = pd.DataFrame({
    'Feature': features,
    'Importance': best_rf.feature_importances_
}).sort_values('Importance', ascending=False)
print("\nRandom Forest Top Features:")
print(rf_importance.head())

gb_importance = pd.DataFrame({
    'Feature': features,
    'Importance': best_gb.feature_importances_
}).sort_values('Importance', ascending=False)
print("\nGradient Boosting Top Features:")
print(gb_importance.head())

# --- 10. Save the Combined Dataset ---
df_combined.to_csv('fully_combined_dataset.csv', index=False)
print("\nCombined dataset saved as 'fully_combined_dataset.csv' for further analysis.")