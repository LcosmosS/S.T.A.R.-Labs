import pandas as pd
import numpy as np
from pathlib import Path
import warnings
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from xgboost import XGBRegressor
from sklearn.metrics import r2_score
import gudhi
import gc


warnings.filterwarnings('ignore')


# ────── FILES ──────
SYNTH_FILE = "synthetic_cosmos_final/synthetic_cosmic_catalog_calibrated.csv"
REAL1_FILE = "JApJ94494_2MASS_GAIADR3_EPOCH.csv"
REAL2_FILE = "DESIDR8_SDSSDR16_SIMBAD.csv"
CHUNK_SIZE = 20000


print("🚀 Starting Step 3 — Full ML + Entropy Cohomology Pipeline")


# Load calibrated synthetic (exact ranks already present)
synth = pd.read_csv(SYNTH_FILE)
print(f"Loaded synthetic: {len(synth):,} galaxies")


# Load real files (chunked)
