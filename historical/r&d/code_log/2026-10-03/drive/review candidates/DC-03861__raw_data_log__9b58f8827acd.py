import pandas as pd
import numpy as np
from sklearn.model_selection import KFold
from xgboost import XGBRegressor
from sklearn.metrics import r2_score, mean_squared_error
from sklearn.neighbors import NearestNeighbors
import gudhi
import warnings
warnings.filterwarnings('ignore')


print("🚀 Step 9 — Full Local Betti_0 / Betti_1 / Betti_2 Pipeline (leakage-free)")


# Load data
synth = pd.read_csv("synthetic_cosmos_final/synthetic_cosmic_catalog_calibrated.csv")
