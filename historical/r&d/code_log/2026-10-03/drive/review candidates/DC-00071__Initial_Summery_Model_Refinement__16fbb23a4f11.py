import numpy as np import pandas as pd from sklearn.model_selection import train_test_split, cross_val_score from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor from sklearn.preprocessing import StandardScaler from sklearn.metrics import mean_squared_error, r2_score from sklearn.impute import SimpleImputer import matplotlib.pyplot as plt import psutil import optuna from pysr import PySRRegressor import shap import warnings
warnings.filterwarnings("ignore") # Suppress any future warnings for cleaner output
# ------------------------------- # Helper: System Resource Monitor
def check_system_resources(): memory = psutil.virtual_memory() cpu = psutil.cpu_percent(interval=1) print(f"CPU Usage: {cpu}%") print(f"Memory Usage: {memory.percent}%") return cpu, memory.percent
# ------------------------------- # Step 1: Load the GZ dataset
gz_df = pd.read_csv("GZ_gzdv1-2_cleaned.csv", low_memory=False) print("Columns in GZ DataFrame:", gz_df.columns.tolist()) print(gz_df.head())
# ------------------------------- # Step 2: Select and preprocess relevant features
selected_features = ['z', 'rMag', 'Ar', 'Pth100', 'Smooth', 'Featured'] gz_df = gz_df[selected_features].copy()
# Impute missing values
gz_df[selected_features] = SimpleImputer(strategy='mean').fit_transform(gz_df[selected_features])
# ------------------------------- # Step 3: Feature Engineering
gz_df['morph_sum'] = gz_df[['Smooth', 'Featured']].sum(axis=1) gz_df['dust_corrected_mag'] = gz_df['rMag'] - gz_df['Ar']
# Ensure valid magnitude values before applying expected SFR formula
gz_df = gz_df[gz_df['dust_corrected_mag'].notna() & (gz_df['dust_corrected_mag'] < 100)]
# Compute expected SFR and apply log transform to avoid overflow
gz_df['expected_SFR'] = 1e-4 * (10 ** (0.4 * (22 - gz_df['dust_corrected_mag']))) ** 1.4 gz_df['expected_SFR'].replace([np.inf, -np.inf], np.nan, inplace=True) gz_df.dropna(subset=['expected_SFR'], inplace=True)
# Apply log transformation to expected_SFR to avoid numerical instability
gz_df['expected_SFR'] = np.log1p(gz_df['expected_SFR']) # log1p for safety
# Define features and target
X = gz_df[['z', 'rMag', 'Ar', 'Pth100', 'morph_sum']] y = gz_df['expected_SFR']
# ------------------------------- # Step 4: Train-test split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
# ------------------------------- # Step 5: Standardize features
scaler = StandardScaler() X_train_scaled = scaler.fit_transform(X_train) X_test_scaled = scaler.transform(X_test)
# ------------------------------- # Step 6: Random Forest - Optuna
check_system_resources()
best_rf = None try: def objective_rf(trial): model = RandomForestRegressor( max_depth=trial.suggest_int("max_depth", 5, 30), n_estimators=trial.suggest_int("n_estimators", 50, 500), min_samples_split=trial.suggest_int("min_samples_split", 2, 20), random_state=42, n_jobs=2 ) return np.mean(cross_val_score(model, X_train_scaled, y_train, cv=3, scoring='r2', n_jobs=2))
study_rf = optuna.create_study(direction="maximize")
study_rf.optimize(objective_rf, n_trials=50)


best_rf = RandomForestRegressor(**study_rf.best_params, random_state=42, n_jobs=2)
best_rf.fit(X_train_scaled, y_train)
