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
from sklearn.preprocessing import QuantileTransformer, RobustScaler




warnings.filterwarnings('ignore')


print(" — v3.5 — Full Upgraded Pipeline with Enhancements")
print(" — Initiating...")


# ====================== 1. LOAD DATA ======================
def load_data():
    CHUNK_SIZE = int(20000) 
    SAMPLE_SIZE = int(50000)
    SEED = int(42)


    # Load synthetic catalog (ensure this file exists in your directory)
    synth = pd.read_csv("synthetic_cosmic_catalog_calibrated.csv")


    # 1. Load Real Catalogs
    real1 = pd.concat([
        chunk for chunk in pd.read_csv(
            "lmfdb_raw_parsed.csv", 
            chunksize=CHUNK_SIZE, 
            low_memory=False
        )
    ], ignore_index=True)


    real2 = pd.concat([
        chunk for chunk in pd.read_csv(
            "lmfdb_3selmer_full_pari.csv", 
            chunksize=CHUNK_SIZE, 
            low_memory=False
        )
    ], ignore_index=True)


    # 2. Sampling and cleaning
    real1 = real1.sample(min(SAMPLE_SIZE, len(real1)), random_state=SEED).reset_index(drop=True)
    
    return synth, real1, real2


# ====================== 2. FORMAL ACSC + TUNABLE β ======================
class ProjectionEngine:
    def __init__(self, beta=16.263, lambda_scale=1.0):
        self.ALPHA = np.sqrt(1.5)
        self.BETA = beta
        self.LAMBDA = lambda_scale


    def apply(self, seed, t_cosmo):
        delta = getattr(seed, 'discriminant', seed.conductor * 10)
        conductor = seed.conductor
        pass
        
        # Geometry remains consistent
        theta = np.mod(np.log10(abs(delta) + 1) * 2 * np.pi, 2 * np.pi)
        phi = np.mod(np.log10(conductor + 1) * np.pi, np.pi)
        
        # --- NEW CORE LOGIC (Complexity 14 + Betti Ratio) ---
        b_ratio = seed.rank / (np.log10(conductor + 1) + 1e-8)
        
        # Discovered Equation of State
        inner_force = ((b_ratio**2 - t_cosmo) + (np.exp(t_cosmo) * 0.4032)) / 0.4610
        z_projected = self.LAMBDA * (1.0 / (np.exp(inner_force) + 1e-9))
        # ----------------------------------------------------


        x = z_projected * np.sin(phi) * np.cos(theta)
        y = z_projected * np.sin(phi) * np.sin(theta)
        z = z_projected * np.cos(phi)
        return np.array([x, y, z])
# --- APPLY ACSC PROJECTION ---
# We generate RA/DE/z proxies for the topology engine
engine = ProjectionEngine()
synth, real1, real2 = load_data()


# Calculate the projection components
# theta (RA proxy), phi (Dec proxy), z_projected (Redshift proxy)
synth['theta'] = np.mod(np.log10(np.abs(synth['discriminant']) + 1) * 2 * np.pi, 2 * np.pi)
synth['phi_angle'] = np.mod(np.log10(synth['conductor'] + 1) * np.pi, np.pi)
    
# Core Equation of State for Redshift
b_ratio = synth['rank'] / (np.log10(synth['conductor'] + 1) + 1e-8)
t_cosmo_dummy = 0.5 # Baseline T_cosmo for projection
inner_force = ((b_ratio**2 - t_cosmo_dummy) + (np.exp(t_cosmo_dummy) * 0.4032)) / 0.4610
    
synth['synthetic_z'] = 1.0 / (np.exp(inner_force) + 1e-9)
synth['synthetic_RA'] = np.rad2deg(synth['theta'])
synth['synthetic_DE'] = np.rad2deg(np.pi/2 - synth['phi_angle'])
    
# Map 'rank' to 'exact_rank' for consistency with later calls
synth['exact_rank'] = synth['rank']
    
# Calculate tda_weight (BSD refinement)
epsilon = 1e-9 
synth['tda_weight'] = np.log1p(synth['regulator'] / (synth['torsion_order']**2 + epsilon))


# ====================== 3. LEAKAGE-FREE FEATURES + BETTI-0 ======================


def add_thesis_features(df, target_col=None):
    df = df.copy()
    df['flux_gr'] = df.get('Gmag', 0) / (df.get('Jmag', 1) + 1e-8)
    df['pm_mag_proxy'] = np.sqrt(df.get('pmRA', 0)**2 + df.get('pmDE', 0)**2)
    df['mag_ratio'] = df.get('gmag', 0) / (df.get('rmag', 1) + 1e-8)
    
    if 'Vcmb' in df.columns:
        df['Tully_Fisher'] = df.get('gmag', 0) + 5 * np.log10(df['Vcmb'] / 100.0)
    else:
        df['Tully_Fisher'] = df.get('gmag', 0)
    
    if 'local_density' in df.columns:
        df['Anthropic'] = np.abs(df['local_density'] - df['local_density'].median())
    else:
        df['Anthropic'] = 0.0
    
    if target_col != 'zphot' and 'zphot' in df.columns:
        df['T_cosmo'] = 1.0 / (1.0 + df['zphot'])
    elif 'Vcmb' in df.columns:
        df['T_cosmo'] = 1.0 / (1.0 + df['Vcmb'] / 3e5)
    else:
        df['T_cosmo'] = 1.0
    
    for col in ['flux_gr', 'pm_mag_proxy', 'mag_ratio', 'Tully_Fisher', 'Anthropic', 'T_cosmo']:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0).astype(float)
    return df


def add_comprehensive_proxies(df, coords, dists, indices, target_col=None):
    """
    Combines intrinsic photometric proxies with extrinsic structural geometry.
