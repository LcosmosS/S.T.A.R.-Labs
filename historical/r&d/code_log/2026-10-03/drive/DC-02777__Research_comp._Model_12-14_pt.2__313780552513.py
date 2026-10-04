import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.impute import SimpleImputer
import matplotlib.pyplot as plt
import psutil
import optuna
from pysr import PySRRegressor
import shap


# -------------------------------
# Helper: System Resource Monitor
def check_system_resources():
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


# Kennicutt-Schmidt Law proxy
df['gas_density'] = 10 ** (0.4 * (22 - df['r']))
A = 1e-4
df['expected_SFR'] = A * (df['gas_density'] ** 1.4)


# Define features and target
X = df[['ra', 'dec', 'u_g', 'g_r', 'r_i', 'i_z', 'expected_SFR']]
y = df['expected_SFR']  # Target is SFR


# -------------------------------
# Step 4: Train-test split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)


# -------------------------------
# Step 5: Standardize features
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)


# -------------------------------
# Step 6: Random Forest - Optuna
check_system_resources()


def objective_rf(trial):
    max_depth = trial.suggest_int("max_depth", 5, 30)
    n_estimators = trial.suggest_int("n_estimators", 50, 500)
    min_samples_split = trial.suggest_int("min_samples_split", 2, 20)
    model = RandomForestRegressor(max_depth=max_depth, n_estimators=n_estimators, min_samples_split=min_samples_split, random_state=42, n_jobs=-1)
    from sklearn.model_selection import cross_val_score
    scores = cross_val_score(model, X_train_scaled, y_train, cv=3, scoring='r2', n_jobs=-1)
    return np.mean(scores)


study_rf = optuna.create_study(direction="maximize")
study_rf.optimize(objective_rf, n_trials=50)


best_rf = RandomForestRegressor(**study_rf.best_params, random_state=42, n_jobs=-1)
best_rf.fit(X_train_scaled, y_train)


# -------------------------------
# Step 7: Gradient Boosting - Optuna
def objective_gb(trial):
    max_depth = trial.suggest_int("max_depth", 3, 20)
    n_estimators = trial.suggest_int("n_estimators", 50, 500)
    min_samples_split = trial.suggest_int("min_samples_split", 2, 20)
    learning_rate = trial.suggest_loguniform("learning_rate", 0.01, 0.3)
    model = GradientBoostingRegressor(max_depth=max_depth, n_estimators=n_estimators, min_samples_split=min_samples_split, learning_rate=learning_rate, random_state=42)
    from sklearn.model_selection import cross_val_score
    scores = cross_val_score(model, X_train_scaled, y_train, cv=3, scoring='r2', n_jobs=-1)
    return np.mean(scores)


study_gb = optuna.create_study(direction="maximize")
study_gb.optimize(objective_gb, n_trials=50)


best_gb = GradientBoostingRegressor(**study_gb.best_params, random_state=42)
best_gb.fit(X_train_scaled, y_train)


# -------------------------------
# Step 8: Evaluate Models
y_pred_rf = best_rf.predict(X_test_scaled)
mse_rf = mean_squared_error(y_test, y_pred_rf)
r2_rf = r2_score(y_test, y_pred_rf)


y_pred_gb = best_gb.predict(X_test_scaled)
mse_gb = mean_squared_error(y_test, y_pred_gb)
r2_gb = r2_score(y_test, y_pred_gb)


print(f"Random Forest - MSE: {mse_rf}, R²: {r2_rf}")
print(f"Gradient Boosting - MSE: {mse_gb}, R²: {r2_gb}")


# -------------------------------
# Step 9: SHAP Analysis
explainer_rf = shap.Explainer(best_rf)
shap_values_rf = explainer_rf(X_test_scaled)
shap.summary_plot(shap_values_rf, X_test, feature_names=X.columns, show=False)
plt.title("SHAP Summary - Random Forest")
plt.savefig("shap_summary_rf.png")


explainer_gb = shap.Explainer(best_gb)
shap_values_gb = explainer_gb(X_test_scaled)
shap.summary_plot(shap_values_gb, X_test, feature_names=X.columns, show=False)
plt.title("SHAP Summary - Gradient Boosting")
plt.savefig("shap_summary_gb.png")


# -------------------------------
# Step 10: Symbolic Regression with PySR
symbolic_model = PySRRegressor(
    model_selection="best",
    niterations=100,
    population_size=1000,
    binary_operators=["+", "-", "*", "/"],
    unary_operators=["sqrt", "log", "exp"],
    loss="loss(x, y) = (x - y)^2",
    maxsize=20,
    verbosity=1,
    random_state=42
)


symbolic_model.fit(X_train, y_train)
print("Best symbolic models:\n", symbolic_model)


# Predict and evaluate
y_pysr_pred = symbolic_model.predict(X_test)
r2_pysr = r2_score(y_test, y_pysr_pred)
print(f"PySR R² score: {r2_pysr:.4f}")


# Save model and expressions
symbolic_model.save("pysr_model.pkl")
symbolic_model.equations_.to_csv("pysr_equations.csv", index=False)


# -------------------------------
# Final system resource check
check_system_resources()
