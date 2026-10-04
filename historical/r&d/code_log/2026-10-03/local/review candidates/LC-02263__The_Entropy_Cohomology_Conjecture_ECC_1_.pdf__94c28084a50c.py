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
    "GradientBoosting": GradientBoostingRegressor(n_estimators=300, learning_rate=0.03,
max_depth=8),
    "CatBoost": CatBoostRegressor(iterations=300, learning_rate=0.05, depth=7, verbose=False),
    "LightGBM": lgb.LGBMRegressor(n_estimators=300, learning_rate=0.03, num_leaves=64),