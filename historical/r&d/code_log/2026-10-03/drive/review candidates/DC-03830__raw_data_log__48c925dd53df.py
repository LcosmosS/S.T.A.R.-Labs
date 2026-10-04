import pandas as pd
import numpy as np
from sklearn.model_selection import KFold, cross_val_score
from xgboost import XGBRegressor
from sklearn.metrics import r2_score, mean_squared_error
import warnings
warnings.filterwarnings('ignore')


print("🚀 Step 4 — Leakage-Free + MSE + 5-Fold CV Pipeline")


# Load data (same as before)
synth = pd.read_csv("synthetic_cosmos_final/synthetic_cosmic_catalog_calibrated.csv")
