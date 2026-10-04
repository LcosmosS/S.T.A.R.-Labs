import optuna
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import cross_val_score
from sklearn.metrics import r2_score
from sklearn.model_selection import KFold
import numpy as np


def objective(trial):
    # Suggest values for hyperparameters
    max_depth = trial.suggest_int("max_depth", 5, 30)
    n_estimators = trial.suggest_int("n_estimators", 50, 500)
    min_samples_split = trial.suggest_int("min_samples_split", 2, 20)


    model = RandomForestRegressor(
        max_depth=max_depth,
        n_estimators=n_estimators,
        min_samples_split=min_samples_split,
        n_jobs=-1,
        random_state=42
    )


    # Use 3-fold CV
    scores = cross_val_score(model, X, y, cv=3, scoring='r2')
    return np.mean(scores)


study = optuna.create_study(direction="maximize")
study.optimize(objective, n_trials=50)  # or more!


print("Best hyperparameters:", study.best_params)
print("Best R² score:", study.best_value)
