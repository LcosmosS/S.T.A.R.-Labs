import pandas as pd
import numpy as np
from sklearn.model_selection import KFold
from sklearn.metrics import r2_score, mean_squared_error
from sklearn.neighbors import NearestNeighbors
from sklearn.svm import SVR
from sklearn.linear_model import Ridge
import xgboost as xgb
import lightgbm as lgb
import gudhi
import optuna
import warnings
warnings.filterwarnings('ignore')


print("🚀 Step 18 — Optuna + Full S.T.A.R. Stacking + PySR Injection + Betti_2")


# Load data (same as before)
synth = pd.read_csv("synthetic_cosmos_final/synthetic_cosmic_catalog_calibrated.csv")
