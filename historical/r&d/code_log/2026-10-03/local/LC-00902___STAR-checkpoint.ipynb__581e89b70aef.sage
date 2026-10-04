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
from sklearn.linear_model import Ridge, Lasso
from sklearn.ensemble import RandomForestClassifier
from sklearn.impute import KNNImputer
from joblib import Parallel, delayed
from scipy.stats import wasserstein_distance

warnings.filterwarnings('ignore')

print(" — *S.T.A.R. + SMAT v3.1 — Full Upgraded Pipeline (SVR + LGBM Optimized)")
print(" — Initiating...")

# ====================== 1. LOAD DATA ======================
def load_data():
    synth = pd.read_csv("synthetic_cosmic_catalog_calibrated.csv")
    real1 = pd.read_csv("JApJ94494_2MASS_GAIADR3_EPOCH.csv", low_memory=False)
    real2 = pd.read_csv("DESIDR8_SDSSDR16_SIMBAD.csv", low_memory=False)
    SAMPLE_SIZE = 25000
    SEED = int(42)
    real1 = real1.sample(SAMPLE_SIZE, random_state=SEED).reset_index(drop=True)
    real2 = real2.sample(SAMPLE_SIZE, random_state=SEED).reset_index(drop=True)
    return synth, real1, real2

synth, real1, real2 = load_data()

# ====================== 2. PROJECTION ENGINE ======================
class ProjectionEngine:
    def __init__(self, beta=16.263, lambda_scale=1.0):
        self.ALPHA = np.sqrt(1.5)
        self.BETA = beta
        self.LAMBDA = lambda_scale

    def apply(self, rank, regulator, conductor, discriminant, t_cosmo):
        theta = np.mod(np.log10(abs(discriminant) + 1) * 2 * np.pi, 2 * np.pi)
        phi = np.mod(np.log10(conductor + 1) * np.pi, np.pi)
        tf_proxy = (rank * self.ALPHA) + np.log(regulator + 1.1)
        z_projected = self.LAMBDA * ((t_cosmo * tf_proxy) + self.ALPHA) - (t_cosmo * self.BETA)
        return z_projected * np.sin(phi) * np.cos(theta), \
               z_projected * np.sin(phi) * np.sin(theta), \
               z_projected * np.cos(phi)

# ====================== 3. FEATURE ENGINEERING ======================
def add_thesis_features(df, target_col=None):
    df = df.copy()
    
    # Pre-cast important columns to standard numpy floats to strip Sage wrappers
    for col in ['Gmag', 'Jmag', 'gmag', 'rmag', 'Vcmb', 'zphot', 'pmRA', 'pmDE']:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce').astype(float)

    df['flux_gr'] = df.get('Gmag', 0.0) / (df.get('Jmag', 1.0) + 1e-8)
    df['pm_mag_proxy'] = np.sqrt(df.get('pmRA', 0.0)**2 + df.get('pmDE', 0.0)**2)
    df['mag_ratio'] = df.get('gmag', 0.0) / (df.get('rmag', 1.0) + 1e-8)
    
    if 'Vcmb' in df.columns:
        # We use standard Python math or ensure numpy array input to avoid Sage conflict
        v_vals = df['Vcmb'].values 
        g_vals = df.get('gmag', 0.0).values if isinstance(df.get('gmag'), pd.Series) else df.get('gmag', 0.0)
        # Apply clipping and log10 on the raw numpy array
        df['Tully_Fisher'] = g_vals + 5.0 * np.log10(np.clip(v_vals, 1e-5, None) / 100.0)
    else:
        df['Tully_Fisher'] = df.get('gmag', 0.0)
    
    if target_col != 'zphot' and 'zphot' in df.columns:
        df['T_cosmo'] = 1.0 / (1.0 + df['zphot'])
    elif 'Vcmb' in df.columns:
        df['T_cosmo'] = 1.0 / (1.0 + df['Vcmb'] / 300000.0)
    else:
        df['T_cosmo'] = 1.0
    
    cols = ['flux_gr', 'pm_mag_proxy', 'mag_ratio', 'Tully_Fisher', 'T_cosmo']
    df[cols] = df[cols].fillna(0.0).astype(float)
    return df

# ====================== 4. TOPOLOGY ======================
def persistence_entropy(diag):
    lifetimes = [d - b for b, d in diag if np.isfinite(d) and d > b + 1e-8]
    if not lifetimes or np.isclose(sum(lifetimes), 0): return 0.0
    p = np.array(lifetimes) / sum(lifetimes)
    return -np.sum(p * np.log(p + 1e-10))

def compute_topology_worker(i, coords, indices, adaptive_scale):
    local_points = coords[indices[i]]
    rips = gudhi.RipsComplex(points=local_points, max_edge_length=adaptive_scale)
    st = rips.create_simplex_tree(max_dimension=2)
    st.compute_persistence()
    betti = st.betti_numbers()
    entropy = persistence_entropy(st.persistence_intervals_in_dimension(1))
    return [betti[0] if len(betti) > 0 else 0,
            betti[1] if len(betti) > 1 else 0,
            betti[2] if len(betti) > 2 else 0,
            entropy]

def add_optimized_topology(df, name, ra_col, de_col, z_col, k=25):
    print(f"Computing {name} topology...")
    z = (df[z_col].values / 3e5) if z_col == 'Vcmb' else df[z_col].values
    dist = z * 4285.7
    ra, de = np.deg2rad(df[ra_col].fillna(0)), np.deg2rad(df[de_col].fillna(0))
    coords = np.column_stack((dist*np.cos(de)*np.cos(ra), dist*np.cos(de)*np.sin(ra), dist*np.sin(de)))
    
    nn = NearestNeighbors(n_neighbors=k).fit(coords)
    dists, indices = nn.kneighbors(coords)
    scale = np.percentile(dists[:, -1], 50)
    
    res = np.array(Parallel(n_jobs=-1)(delayed(compute_topology_worker)(i, coords, indices, scale) for i in range(len(coords))))
    df['local_betti_0'], df['local_betti_1'], df['local_betti_2'], df['persistence_entropy'] = res.T
    df['Anthropic'] = np.abs(dists.mean(axis=1) - np.median(dists.mean(axis=1)))
    
    if df['persistence_entropy'].nunique() > 1:
        df['entropy_strata'] = (df['persistence_entropy'].rank(pct=True, method='first') * 2.99).astype(int)
    else:
        df['entropy_strata'] = 1
    return df

# ====================== 5. THE STACKER (LGBM + SVR) ======================
class RefinedECCStacker:
    def __init__(self, xgb_p, lgb_p):
        self.base_models = [
            ('xgb', xgb.XGBRegressor(**xgb_p)),
            ('lgb', lgb.LGBMRegressor(**lgb_p))
        ]
        # HETEROGENEOUS META-MODELS
        self.meta_models = {
            0: Lasso(alpha=2.0), # Quenches Stratum 0 noise
            1: Ridge(alpha=1.0), # Linear for transition
            2: SVR(kernel='rbf', C=10) # Non-linear for high-rank voids
        }
        self.strata_clf = RandomForestClassifier(n_estimators=100, max_depth=4)

    def fit(self, X, y, strata):
        self.strata_clf.fit(X, strata)
        # Train base learners
        preds = np.column_stack([m[1].fit(X, y).predict(X) for m in self.base_models])
        
        for s in [0, 1, 2]:
            mask = (strata == s)
            if mask.sum() > 10:
                # If target variance is near zero (Stratum 0), force a constant
                if np.std(y[mask]) < 1e-4:
                    self.meta_models[s] = "constant_zero"
                else:
                    self.meta_models[s].fit(preds[mask], y[mask])

    def predict(self, X):
        s_pred = self.strata_clf.predict(X)
        b_pred = np.column_stack([m[1].predict(X) for m in self.base_models])
        final = np.zeros(len(X))
        for s in [0, 1, 2]:
            mask = (s_pred == s)
            if mask.sum() > 0:
                if self.meta_models[s] == "constant_zero":
                    final[mask] = 0.0
                else:
                    final[mask] = self.meta_models[s].predict(b_pred[mask])
        return final

# ====================== 2. BETA ALIGNMENT ======================
# New Hall of Fame Refined Beta
REFINED_BETA = 16.20 
print(f"Applying Refined Foliation Beta: {REFINED_BETA}")

# ====================== EXECUTION ======================
synth = add_thesis_features(synth)
real1 = add_thesis_features(real1)
real2 = add_thesis_features(real2, target_col='zphot')

synth = add_optimized_topology(synth, "synth", "synthetic_RA", "synthetic_DE", "synthetic_z")
real1 = add_optimized_topology(real1, "real1", "RAJ2000", "DEJ2000", "Vcmb")
real2 = add_optimized_topology(real2, "real2", "RAdeg", "DEdeg", "zphot")

common_features = ['flux_gr', 'pm_mag_proxy', 'mag_ratio', 'Tully_Fisher', 'Anthropic', 'T_cosmo', 'local_betti_0', 'local_betti_1', 'local_betti_2']
imputer = KNNImputer(n_neighbors=10)
for df in [synth, real1, real2]: df[common_features] = imputer.fit_transform(df[common_features])

# Multi-Learner Optuna
def objective(trial):
    xgb_p = {'n_estimators': trial.suggest_int('x_n', 400, 600), 'learning_rate': trial.suggest_float('x_lr', 0.01, 0.05), 'max_depth': trial.suggest_int('x_d', 4, 6)}
    lgb_p = {'n_estimators': trial.suggest_int('l_n', 400, 600), 'learning_rate': trial.suggest_float('l_lr', 0.01, 0.05), 'num_leaves': trial.suggest_int('l_lv', 15, 31), 'verbose': -1}
    
    kf = KFold(n_splits=int(3), shuffle=True, random_state=int(42))
    scores = []
    for tr, val in kf.split(synth):
        m1 = xgb.XGBRegressor(**xgb_p).fit(synth[common_features].iloc[tr], synth['exact_rank'].iloc[tr])
        m2 = lgb.LGBMRegressor(**lgb_p).fit(synth[common_features].iloc[tr], synth['exact_rank'].iloc[tr])
        p = (m1.predict(synth[common_features].iloc[val]) + m2.predict(synth[common_features].iloc[val])) / 2
        scores.append(mean_squared_error(synth['exact_rank'].iloc[val], p) + wasserstein_distance(synth['exact_rank'].iloc[val], p))
    return np.mean(scores)

study = optuna.create_study(direction='minimize')
study.optimize(objective, n_trials=int(10))

# Final Deployment
x_best = {k[2:]: v for k, v in study.best_params.items() if k.startswith('x_')}
l_best = {k[2:]: v for k, v in study.best_params.items() if k.startswith('l_')}
l_best['verbose'] = -1

global_stacker = StableECCStacker(x_best, l_best)
global_stacker.fit(real2[common_features], real2['persistence_entropy'], real2['entropy_strata'])

# Foliation R2 Analysis
print("\n--- Final Multi-Strata R² (With SVR Meta-Learner) ---")
preds = global_stacker.predict(real2[common_features])
for s in [0, 1, 2]:
    mask = (real2['entropy_strata'] == s)
    print(f"Stratum {s} R²: {r2_score(real2['persistence_entropy'][mask], preds[mask]):.4f}")

# Histogram of Discovered Constants
plt.figure(figsize=(8, 4))
plt.hist(np.log(np.abs([16.263, np.sqrt(1.5), 1.22, 1.35]) + 1e-8), color='teal')
plt.title("Spectral Distribution of Model Constants")
plt.show()