import pandas as pd
import numpy as np
import warnings
import gudhi
import optuna
import xgboost as xgb
import lightgbm as lgb
import catboost as cb
from tqdm import tqdm  # Added for visibility

from sklearn.model_selection import KFold
from sklearn.metrics import r2_score
from sklearn.neighbors import NearestNeighbors
from sklearn.linear_model import Ridge
from sklearn.impute import KNNImputer
from joblib import Parallel, delayed
from pysr import PySRRegressor

warnings.filterwarnings('ignore')

print(" — *S.T.A.R. Program: v2.2 (Performance Optimized)")
print(" — Initiating...")

# ====================== 1. DATA LOADING & SAMPLING ======================
def load_data():
    synth = pd.read_csv("synthetic_cosmic_catalog_calibrated.csv")
    real1 = pd.read_csv("JApJ94494_2MASS_GAIADR3_EPOCH.csv", low_memory=False)
    real2 = pd.read_csv("DESIDR8_SDSSDR16_SIMBAD.csv", low_memory=False)
    
    # PERFORMANCE FIX: Downsample huge catalogs to tractable limits
    # ACSC suggests Wasserstein distances stabilize at ~15k-20k samples 
    for name, df in [("Real1", real1), ("Real2", real2)]:
        if len(df) > 25000:
            print(f" {name} is too large ({len(df)} rows). Sampling 25,000 rows for tractability.")
            df = df.sample(25000, random_state=42).reset_index(drop=True)
            if name == "Real1": real1 = df
            else: real2 = df
            
    return synth, real1, real2

# ====================== 2. FEATURE ENGINEERING ======================
def add_thesis_features(df):
    df = df.copy()
    # Standard S.T.A.R. Invariants [cite: 13, 16]
    df['flux_gr'] = df.get('Gmag', 0) / (df.get('Jmag', 1) + 1e-8)
    df['pm_mag_proxy'] = np.sqrt(df.get('pmRA', 0)**2 + df.get('pmDE', 0)**2)
    df['mag_ratio'] = df.get('gmag', 0) / (df.get('rmag', 1) + 1e-8)
    
    if 'zphot' in df.columns:
        df['T_cosmo'] = 1.0 / (1.0 + df['zphot'])
    elif 'Vcmb' in df.columns:
        df['T_cosmo'] = 1.0 / (1.0 + df['Vcmb'] / 3e5)
    else:
        df['T_cosmo'] = 1.0 / (1.0 + df.get('synthetic_z', 0))
        
    v_val = df.get('Vcmb', df.get('synthetic_z', 0) * 3e5)
    df['Tully_Fisher'] = df.get('gmag', 0) + 5 * np.log10(np.maximum(v_val / 100.0, 1e-5))
    return df

# ====================== 3. TOPOLOGY (BATCHED PARALLEL) ======================
def compute_betti_worker(points, scale):
    try:
        rips = gudhi.RipsComplex(points=points, max_edge_length=scale)
        st = rips.create_simplex_tree(max_dimension=2)
        st.compute_persistence()
        b = st.betti_numbers()
        return [b[j] if len(b) > j else 0 for j in range(3)]
    except:
        return [0, 0, 0]

def add_optimized_topology(df, name, ra_col, de_col, z_col, k=25):
    print(f" — *S.T.A.R. Computing {name} topology...")
    z = (df[z_col].values / 3e5) if z_col == 'Vcmb' else df[z_col].values
    comoving_dist = np.nan_to_num(z * 4285.7)
    ra_rad, de_rad = np.deg2rad(df[ra_col].fillna(0)), np.deg2rad(df[de_col].fillna(0))
    
    coords = np.column_stack((
        comoving_dist * np.cos(de_rad) * np.cos(ra_rad),
        comoving_dist * np.cos(de_rad) * np.sin(ra_rad),
        comoving_dist * np.sin(de_rad)
    ))

    nn = NearestNeighbors(n_neighbors=k).fit(coords)
    dists, indices = nn.kneighbors(coords)
    adaptive_scale = np.percentile(dists[:, -1], 50)
    
    # PERFORMANCE FIX: Use batching to reduce Parallel overhead
    # This provides the Betti 0 (voids), 1 (filaments), and 2 (clusters) required by ACSC 
    results = Parallel(n_jobs=-1, batch_size=50)(
        delayed(compute_betti_worker)(coords[indices[i]], adaptive_scale) 
        for i in tqdm(range(len(coords)), desc=f"   {name} Topology")
    )
    betti_arr = np.array(results)
    
    df['local_betti_2_std'] = betti_arr[:, 2]
    df['local_betti_1_std'] = betti_arr[:, 1]
    df['local_density'] = dists.mean(axis=1)
    df['Anthropic'] = np.abs(df['local_density'] - np.median(df['local_density']))
    return df

# ====================== 4. EXECUTION ======================
synth, real1, real2 = load_data()

synth = add_thesis_features(synth)
real1 = add_thesis_features(real1)
real2 = add_thesis_features(real2)

synth = add_optimized_topology(synth, "Synthetic", "synthetic_RA", "synthetic_DE", "synthetic_z")
real1 = add_optimized_topology(real1, "JApJ (Real1)", "RAJ2000", "DEJ2000", "Vcmb")
real2 = add_optimized_topology(real2, "DESI (Real2)", "RAdeg", "DEdeg", "zphot")

# Standardization & KNN Imputation
common_features = ['flux_gr', 'pm_mag_proxy', 'mag_ratio', 'T_cosmo', 'Tully_Fisher', 'Anthropic', 'local_betti_2_std']
imputer = KNNImputer(n_neighbors=10)
for df in [synth, real1, real2]:
    df[common_features] = imputer.fit_transform(df[common_features])

# ====================== 5. OPTUNA & PySR (TRAINED ON SYNTHETIC) ======================
def objective(trial):
    param = {
        'n_estimators': trial.suggest_int('n_estimators', 400, 800),
        'learning_rate': trial.suggest_float('learning_rate', 0.01, 0.05),
        'max_depth': trial.suggest_int('max_depth', 4, 7),
        'random_state': 42
    }
    kf = KFold(n_splits=5, shuffle=True)
    scores = []
    for tr, val in kf.split(synth):
        model = xgb.XGBRegressor(**param)
        model.fit(synth[common_features].iloc[tr], synth_y.iloc[tr])
        scores.append(r2_score(synth_y.iloc[val], model.predict(synth[common_features].iloc[val])))
    return np.mean(scores)

print("\n — *S.T.A.R. Running Optuna...")
study = optuna.create_study(direction='maximize')
study.optimize(objective, n_trials=20)
best_params = study.best_params

print("\n — *S.T.A.R. Fitting PySR (Synthetic Anchor)...")
pysr = PySRRegressor(niterations=40, maxsize=12, random_state=42)
pysr.fit(synth[common_features], synth_y)

# Inject symbolic signal
for df in [synth, real1, real2]:
    # Because common_features match exactly, PySR won't create NaNs anymore
    df['pysr_signal'] = pysr.predict(df[common_features])

common_features.append('pysr_signal')

# ====================== 6. FINAL STACKED EVALUATION ======================
def run_stack(df, y, name):
    X = df[common_features]
    estimators = [
        ('xgb', xgb.XGBRegressor(**best_params)),
        ('lgb', lgb.LGBMRegressor(n_estimators=400, verbose=-1)),
        ('cat', cb.CatBoostRegressor(iterations=400, silent=True))
    ]
    stack = StackingRegressor(estimators=estimators, final_estimator=Ridge())
    
    kf = KFold(n_splits=5, shuffle=True, random_state=42)
    r2_list = []
    for tr, val in kf.split(X):
        stack.fit(X.iloc[tr], y.iloc[tr])
        r2_list.append(r2_score(y.iloc[val], stack.predict(X.iloc[val])))
    
    print(f" {name} Stacked R²: {np.mean(r2_list):.4f}")

run_stack(synth, synth_y, "Synthetic")
run_stack(real1, real1_y, "Real1 (JApJ)")
run_stack(real2, real2_y, "Real2 (DESI)")

print("\n — Processing Complete — ")