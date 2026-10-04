import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.impute import SimpleImputer
import matplotlib.pyplot as plt
import psutil  # For monitoring system resources
import optuna  # For Bayesian optimization
from scipy.stats import randint
from numpy.polynomial.polynomial import Polynomial


# -------------------------------
# Helper: System Resource Monitor
def check_system_resources():
    import psutil
    memory = psutil.virtual_memory()
    cpu = psutil.cpu_percent(interval=1)
    print(f"CPU Usage: {cpu}%")
    print(f"Memory Usage: {memory.percent}%")
    return cpu, memory.percent


# -------------------------------
# Step 1: Load the SDSS dataset
df = pd.read_csv('SDSSDR18_200000.csv', low_memory=False)
print("Columns in SDSS DataFrame:", df.columns)
print(df.head())


# -------------------------------
# Step 2: Data Preprocessing
# Impute missing values for selected columns
imputer = SimpleImputer(strategy='mean')
cols_to_impute = ['ra', 'dec', 'redshift', 'u', 'g', 'r', 'i', 'z']
df[cols_to_impute] = imputer.fit_transform(df[cols_to_impute])


# -------------------------------
# Step 3: Feature Engineering
# Calculate color indices
df['u_g'] = df['u'] - df['g']
df['g_r'] = df['g'] - df['r']
df['r_i'] = df['r'] - df['i']
df['i_z'] = df['i'] - df['z']


# --- Integrate Kennicutt-Schmidt Law ---
# Here we create a proxy for gas density. This is a rough approximation:
# Assume brighter (lower r magnitude) galaxies have higher gas densities.
# (In practice, you would use direct gas measurements.)
df['gas_density'] = 10 ** (0.4 * (22 - df['r']))  
# Define a normalization constant A (calibrated from literature; adjust as needed)
A = 1e-4  
# Compute expected SFR using the Kennicutt-Schmidt law (power-law index ~1.4)
df['expected_SFR'] = A * (df['gas_density'] ** 1.4)
# If an observed SFR is available, you might compute a residual; otherwise, expected_SFR can be used as a feature


# For this example, we use expected_SFR as an additional feature.
# Also, we'll use redshift as our target (or you could choose another target variable).
# Here, as an example, we predict redshift using photometry (in practice, you might predict SFR).
X = df[['ra', 'dec', 'u_g', 'g_r', 'r_i', 'i_z', 'expected_SFR']]
y = df['redshift']


# -------------------------------
# Step 4: Split data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)


# -------------------------------
# Step 5: Standardize the features
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)


# -------------------------------
# Optional: Monitor system resources before optimization
check_system_resources()


# -------------------------------
# Step 6: Bayesian Optimization with Optuna for RandomForestRegressor
def objective_rf(trial):
    max_depth = trial.suggest_int("max_depth", 5, 30)
    n_estimators = trial.suggest_int("n_estimators", 50, 500)
    min_samples_split = trial.suggest_int("min_samples_split", 2, 20)
    
    model = RandomForestRegressor(
        max_depth=max_depth,
        n_estimators=n_estimators,
        min_samples_split=min_samples_split,
        random_state=42,
        n_jobs=-1
    )
    # Use 3-fold cross-validation and optimize for R² score
    from sklearn.model_selection import cross_val_score
    scores = cross_val_score(model, X_train_scaled, y_train, cv=3, scoring='r2', n_jobs=-1)
    return np.mean(scores)


study_rf = optuna.create_study(direction="maximize")
study_rf.optimize(objective_rf, n_trials=50)


print("Best RandomForest hyperparameters:", study_rf.best_params)
best_rf = RandomForestRegressor(
    **study_rf.best_params, random_state=42, n_jobs=-1
)
best_rf.fit(X_train_scaled, y_train)


# -------------------------------
# Step 7: Bayesian Optimization with Optuna for GradientBoostingRegressor
def objective_gb(trial):
    max_depth = trial.suggest_int("max_depth", 3, 20)
    n_estimators = trial.suggest_int("n_estimators", 50, 500)
    min_samples_split = trial.suggest_int("min_samples_split", 2, 20)
    learning_rate = trial.suggest_loguniform("learning_rate", 0.01, 0.3)
    
    model = GradientBoostingRegressor(
        max_depth=max_depth,
        n_estimators=n_estimators,
        min_samples_split=min_samples_split,
        learning_rate=learning_rate,
        random_state=42
    )
    from sklearn.model_selection import cross_val_score
    scores = cross_val_score(model, X_train_scaled, y_train, cv=3, scoring='r2', n_jobs=-1)
    return np.mean(scores)


study_gb = optuna.create_study(direction="maximize")
study_gb.optimize(objective_gb, n_trials=50)


print("Best GradientBoosting hyperparameters:", study_gb.best_params)
best_gb = GradientBoostingRegressor(
    **study_gb.best_params, random_state=42
)
best_gb.fit(X_train_scaled, y_train)


# -------------------------------
# Step 8: Evaluate Both Models on Test Set
y_pred_rf = best_rf.predict(X_test_scaled)
mse_rf = mean_squared_error(y_test, y_pred_rf)
r2_rf = best_rf.score(X_test_scaled, y_test)


y_pred_gb = best_gb.predict(X_test_scaled)
mse_gb = mean_squared_error(y_test, y_pred_gb)
r2_gb = best_gb.score(X_test_scaled, y_test)


print(f"Random Forest - MSE: {mse_rf}, R²: {r2_rf}")
print(f"Gradient Boosting - MSE: {mse_gb}, R²: {r2_gb}")


# -------------------------------
# Step 9: SHAP Analysis (optional)
import shap
explainer_rf = shap.TreeExplainer(best_rf)
shap_values_rf = explainer_rf.shap_values(X_test_scaled)
shap.summary_plot(shap_values_rf, X_test, feature_names=X.columns)


explainer_gb = shap.TreeExplainer(best_gb)
shap_values_gb = explainer_gb.shap_values(X_test_scaled)
shap.summary_plot(shap_values_gb, X_test, feature_names=X.columns)


# -------------------------------
# Final resource check
check_system_resources()
