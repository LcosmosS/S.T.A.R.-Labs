import pandas as pd
import numpy as np
import warnings
import gudhi
import optuna
import xgboost as xgb
import lightgbm as lgb
import catboost as cb
import matplotlib.pyplot as plt
from sklearn.model_selection import KFold
from sklearn.metrics import r2_score, mean_squared_error
from sklearn.neighbors import NearestNeighbors
from sklearn.svm import SVR
from sklearn.linear_model import Ridge
from sklearn.ensemble import HistGradientBoostingRegressor, RandomForestClassifier
from sklearn.impute import KNNImputer
from joblib import Parallel, delayed
from pysr import PySRRegressor
from scipy.stats import wasserstein_distance
from sklearn.metrics import mean_absolute_error
from sklearn.preprocessing import QuantileTransformer

warnings.filterwarnings('ignore')

print(" — *S.T.A.R. + SMAT v3.5 — Full Upgraded Pipeline with Enhancements")
print(" — Initiating...")

# ====================== 1. LOAD DATA ======================
def load_data():
# Load data
    synth = pd.read_csv("synthetic_cosmic_catalog_calibrated.csv")
    real1 = pd.concat([chunk for chunk in
pd.read_csv("JApJ94494_2MASS_GAIADR3_EPOCH.csv", chunksize=int(20000),
low_memory=False)], ignore_index=True)
    real2 = pd.concat([chunk for chunk in pd.read_csv("DESIDR8_SDSSDR16_SIMBAD.csv",
chunksize=int(20000), low_memory=False)], ignore_index=True)
    SAMPLE_SIZE = 250000
    SEED = int(42)
    real1 = real1.sample(SAMPLE_SIZE, random_state=SEED).reset_index(drop=True)
    real2 = real2.sample(SAMPLE_SIZE, random_state=SEED).reset_index(drop=True)
    return synth, real1, real2

synth, real1, real2 = load_data()
