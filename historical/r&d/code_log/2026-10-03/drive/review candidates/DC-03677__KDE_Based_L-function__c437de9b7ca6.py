import optuna
from optuna.samplers import TPESampler
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import StandardScaler
import pandas as pd
import numpy as np


# Load the filtered dataset
file_path = "\\wsl.localhost\Ubuntu\home\pmqr7\filtered_dataset.csv"
df = pd.read_csv(file_path)


# Drop rows with missing target variable (log_SFR_Ha)
df = df.dropna(subset=["log_SFR_Ha"])


# Select features and target
target = "log_SFR_Ha"
features = df.columns.drop(["log_SFR_Ha", "CATAID", "CATAID.1", "CATAID.2"], errors='ignore')
X = df[features]
y = df[target]


# Scale features
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)


# Split into training and test sets
X_train_scaled, X_test_scaled, y_train, y_test = train_test_split(
    X_scaled, y, test_size=0.2, random_state=42
)


# Diagnostic output to check for data issues
print("X_train_scaled sample:")
print(pd.DataFrame(X_train_scaled).head())
print("X_train_scaled stats:")
print("Min:", np.min(X_train_scaled))
print("Max:", np.max(X_train_scaled))
print("Any NaNs?", np.isnan(X_train_scaled).any())


print("\ny_train sample:")
print(y_train.head())
print("y_train stats:")
print("Min:", y_train.min())
print("Max:", y_train.max())
print("Any NaNs?", y_train.isna().any())


# Define objective function for Optuna
def objective_rf(trial):
    n_estimators = trial.suggest_int("n_estimators", 100, 1000)
    max_depth = trial.suggest_int("max_depth", 5, 50)
    min_samples_split = trial.suggest_int("min_samples_split", 2, 10)
    min_samples_leaf = trial.suggest_int("min_samples_leaf", 1, 10)


    rf = RandomForestRegressor(
        n_estimators=n_estimators,
        max_depth=max_depth,
        min_samples_split=min_samples_split,
        min_samples_leaf=min_samples_leaf,
        random_state=42,
        n_jobs=-1
    )


    score = cross_val_score(rf, X_train_scaled, y_train, cv=5, scoring="r2").mean()
    return score


# Run Optuna study
study = optuna.create_study(direction="maximize", sampler=TPESampler(seed=42))
study.optimize(objective_rf, n_trials=50)


print("Best trial:")
print(study.best_trial)
