import pandas as pd
import numpy as np
import warnings
import gudhi
import optuna
import xgboost as xgb
import lightgbm as lgb
import catboost as cb
from tqdm import tqdm
from sklearn.model_selection import KFold
from sklearn.metrics import r2_score
from sklearn.neighbors import NearestNeighbors
from sklearn.linear_model import Ridge
from sklearn.impute import KNNImputer
from sklearn.ensemble import StackingRegressor
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
    
    SAMPLE_SIZE = int(250000)
    SEED = int(42)
    
    processed_reals = []
    for name, df in [("Real1", real1), ("Real2", real2)]:
        if len(df) > SAMPLE_SIZE:
            print(f" {name} is too large ({len(df)} rows). Sampling {SAMPLE_SIZE} rows.")
            df = df.sample(n=SAMPLE_SIZE, random_state=SEED).reset_index(drop=True)
        processed_reals.append(df)
            
    return synth, processed_reals[0], processed_reals[1]


# ====================== 2. FEATURE ENGINEERING ======================
def add_thesis_features(df):
    df = df.copy()
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


# ====================== 3. TOPOLOGY (PARALLEL BATCHED) ======================
def compute_betti_worker(points, scale):
    try:
        rips =激gudhi.RipsComplex(points=points, max_edge_length=scale)
        st = rips.create_simplex_tree(max_dimension=int(2))
        st.compute_persistence()
        b = st.betti_numbers()
        return [b[j] if len(b) > j else 0 for j in range(3)]
    except:
        return [0, 0, 0]


def add_optimized_topology(df, name, ra_col, de_col, z_col, k=25):
    print(f" Computing {name} topology...")
    k_int = int(k)
    z = (df[z_col].values / 3e5) if z_col == 'Vcmb' else df[z_col].values
    comoving_dist = np.nan_to_num(z * 4285.7)
    ra_rad, de_rad = np.deg2rad(df[ra_col].fillna(0).values), np.deg2rad(df[de_col].fillna(0).values)
    
    coords = np.column_stack((
        comoving_dist * np.cos(de_rad) * np.cos(ra_rad),
        comoving_dist * np.cos(de_rad) * np.sin(ra_rad),
        comoving_dist * np.sin(de_rad)
    ))


    nn = NearestNeighbors(n_neighbors=k_int).fit(coords)
    dists, indices = nn.kneighbors(coords)
    adaptive_scale = np.percentile(dists[:, -1], 50)
    
    results = Parallel(n_jobs=-1, batch_size=int(50))(
        delayed(compute_betti_worker)(coords[indices[i]], adaptive_scale) 
        for i in tqdm(range(len(coords)), desc=f"   {name} Topology")
    )
    
    betti_arr = np.array(results)
    df['local_betti_2_std'] = betti_arr[:, 2]
    df['local_betti_1_std'] = betti_arr[:, 1]
    df['local_density'] = dists.mean(axis=1)
    df['Anthropic'] = np.abs(df['local_density'] - np.median(df['local_density']))
    return df


# ====================== 4. EXECUTION START ======================
synth, real1, real2 = load_data()


synth = add_thesis_features(synth)
real1 = add_thesis_features(real1)
real2 = add_thesis_features(real2)


synth = add_optimized_topology(synth, "Synthetic", "synthetic_RA", "synthetic_DE", "synthetic_z")
real1 = add_optimized_topology(real1, "Real1", "RAJ2000", "DEJ2000", "Vcmb")
real2 = add_optimized_topology(real2, "Real2", "RAdeg", "DEdeg", "zphot")


# Targets (ECC Logic: Rank-Entropy Correlation)
synth_y = synth['exact_rank']
real1_y = real1['exact_rank'] if 'exact_rank' in real1.columns else real1['local_density'] 
real2_y = real2['zphot'] # Proxy for high-z evolution target


# Pre-processing
common_features = ['flux_gr', 'pm_mag_proxy', 'mag_ratio', 'T_cosmo', 'Tully_Fisher', 'Anthropic', 'local_betti_2_std']
imputer = KNNImputer(n_neighbors=int(10))
for df in [synth, real1, real2]:
    df[common_features] = imputer.fit_transform(df[common_features])


# ====================== 5. OPTUNA & PySR (SAGE-FIXED) ======================
def objective(trial):
    param = {
        'n_estimators': int(trial.suggest_int('n_estimators', 400, 800)),
        'learning_rate': float(trial.suggest_float('learning_rate', 0.01, 0.05)),
        'max_depth': int(trial.suggest_int('max_depth', 4, 7)),
        'random_state': int(42)
    }
    kf = KFold(n_splits=int(5), shuffle=True, random_state=int(42))
    scores = []
    for tr, val in kf.split(synth):
        model = xgb.XGBRegressor(**param)
        model.fit(synth[common_features].iloc[tr], synth_y.iloc[tr])
        scores.append(r2_score(synth_y.iloc[val], model.predict(synth[common_features].iloc[val])))
    return np.mean(scores)


print("\n — *S.T.A.R. Running Optuna Hyper-tuning...")
study = optuna.create_study(direction='maximize')
study.optimize(objective, n_trials=int(20))
best_params = study.best_params


print("\n — *S.T.A.R. Fitting PySR (Symbolic Anchor)...")
pysr = PySRRegressor(
    niterations=int(40), 
    maxsize=int(12), 
    random_state=int(42),
    procs=int(4)
)
pysr.fit(synth[common_features], synth_y)


# Inject symbolic signal
for df in [synth, real1, real2]:
    df['pysr_signal'] = pysr.predict(df[common_features])


common_features.append('pysr_signal')


# ====================== 6. FINAL STACKED EVALUATION ======================
def run_stack(df, y, name):
    X = df[common_features]
    estimators = [
        ('xgb', xgb.XGBRegressor(**best_params)),
        ('lgb', lgb.LGBMRegressor(n_estimators=int(400), verbose=int(-1))),
        ('cat', cb.CatBoostRegressor(iterations=int(400), silent=True))
    ]
    stack = StackingRegressor(estimators=estimators, final_estimator=Ridge())
    
    kf = KFold(n_splits=int(5), shuffle=True, random_state=int(42))
    r2_list = []
    for tr, val in kf.split(X):
        stack.fit(X.iloc[tr], y.iloc[tr])
        r2_list.append(r2_score(y.iloc[val], stack.predict(X.iloc[val])))
    
    print(f" {name} Stacked R²: {np.mean(r2_list):.4f}")


run_stack(synth, synth_y, "Synthetic (Seed)")
run_stack(real1, real1_y, "Real1 (2MASS/Gaia)")
run_stack(real2, real2_y, "Real2 (DESI/SDSS)")


print(" Topology computation complete. Proceeding to Symbolic Regression.")
