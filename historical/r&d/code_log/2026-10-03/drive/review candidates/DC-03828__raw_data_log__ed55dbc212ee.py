import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from xgboost import XGBRegressor
from sklearn.metrics import r2_score
import warnings
warnings.filterwarnings('ignore')


# Files
SYNTH_FILE = "synthetic_cosmos_final/synthetic_cosmic_catalog_calibrated.csv"
REAL1_FILE = "JApJ94494_2MASS_GAIADR3_EPOCH.csv"
REAL2_FILE = "DESIDR8_SDSSDR16_SIMBAD.csv"


print("🚀 Step 4 — Leakage-Free ACSC Validation")


# Load data
synth = pd.read_csv(SYNTH_FILE)
