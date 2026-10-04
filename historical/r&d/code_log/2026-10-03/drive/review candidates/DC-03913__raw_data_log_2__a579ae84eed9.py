import pandas as pd
import numpy as np
from sklearn.model_selection import KFold
from sklearn.metrics import r2_score, mean_squared_error
from sklearn.neighbors import NearestNeighbors
from sklearn.svm import SVR
from sklearn.linear_model import Ridge
from sklearn.ensemble import HistGradientBoostingRegressor
import xgboost as xgb
import lightgbm as lgb
import catboost as cb
import gudhi
import optuna
import warnings
warnings.filterwarnings('ignore')


print("🚀 Step 19 — FIXED Expanded Stacking (CatBoost + HistGB + XGBoost + LightGBM + SVR) + PySR Injection")


# ====================== LOAD DATA ======================
synth = pd.read_csv("synthetic_cosmos_final/synthetic_cosmic_catalog_calibrated.csv")
