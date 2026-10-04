import pandas as pd
import numpy as np
from sklearn.model_selection import KFold
from xgboost import XGBRegressor
from sklearn.metrics import r2_score, mean_squared_error
from sklearn.neighbors import NearestNeighbors
import gudhi
import warnings
warnings.filterwarnings('ignore')


print("🚀 Step 11 — Lagrangian 3-Body Proxy + Full Local Betti_0/1/2 (no leakage)")


# Load data
synth = pd.read_csv("synthetic_cosmos_final/synthetic_cosmic_catalog_calibrated.csv")
