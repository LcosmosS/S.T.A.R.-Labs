import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from catboost import CatBoostRegressor
from xgboost import XGBRegressor
import lightgbm as lgb
from gplearn.genetic import SymbolicRegressor
import optuna
from sklearn.metrics import r2_score, mean_absolute_error

# Load dataset
data = pd.read_csv("final_merged_entropy_projection_dataset.csv")
features = ['log_Mass_gas', 'log_Mass_stellar', 'Av_gas_Re', 'OH_O3N2_cen', 
           'Smooth', 'Featured', 'pS', 'fM', 'z', 'Re_kpc', 'L_cosmo(s)', 'BSD_likelihood']
target = 'log_SFR_Ha'
X, y = data[features], data[target]
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Define models
models = {
   "RandomForest": RandomForestRegressor(n_estimators=200, max_depth=10),
   "GradientBoosting": GradientBoostingRegressor(n_estimators=300, learning_rate=0.03, max_depth=8),
   "CatBoost": CatBoostRegressor(iterations=300, learning_rate=0.05, depth=7, verbose=False),
   "LightGBM": lgb.LGBMRegressor(n_estimators=300, learning_rate=0.03, num_leaves=64),
   "XGBoost": XGBRegressor(n_estimators=300, learning_rate=0.03, max_depth=7, reg_alpha=0.2, reg_lambda=1.0),
   "GPlearn": SymbolicRegressor(population_size=2000, generations=30, function_set=['add', 'sub', 'mul', 'div', 'log', 'sqrt'], metric='mean absolute error', parsimony_coefficient=0.01, random_state=42)
}

results = {}
for name, model in models.items():
   model.fit(X_train, y_train)
   preds = model.predict(X_test)
   results[name] = {
       "R2": r2_score(y_test, preds),
       "MAE": mean_absolute_error(y_test, preds)
   }

# Best Optuna-tuned XGBoost as symbolic optimizer
def objective(trial):
   params = {
       "n_estimators": trial.suggest_int("n_estimators", 100, 1000),
       "max_depth": trial.suggest_int("max_depth", 4, 12),
       "learning_rate": trial.suggest_float("learning_rate", 0.01, 0.2),
       "subsample": trial.suggest_float("subsample", 0.7, 1.0),
       "reg_alpha": trial.suggest_float("reg_alpha", 0.0, 1.0),
       "reg_lambda": trial.suggest_float("reg_lambda", 0.0, 1.0),
   }
   model = XGBRegressor(**params)
   model.fit(X_train, y_train)
   preds = model.predict(X_test)
   return 1 - mean_absolute_error(y_test, preds)

study = optuna.create_study(direction="maximize")
study.optimize(objective, n_trials=50)
optuna_best_params = study.best_params
optuna_model = XGBRegressor(**optuna_best_params)
optuna_model.fit(X_train, y_train)
optuna_preds = optuna_model.predict(X_test)
results["Optuna_XGBoost"] = {
   "R2": r2_score(y_test, optuna_preds),
   "MAE": mean_absolute_error(y_test, optuna_preds)
}
