import pandas as pd
import numpy as np
from sklearn.model_selection import KFold
from xgboost import XGBRegressor
from sklearn.metrics import r2_score, mean_squared_error
from sklearn.neighbors import NearestNeighbors
import gudhi
import warnings
warnings.filterwarnings('ignore')

print(" — Full Persistent Homology + Local Betti_0/1/2 + Thesis Metrics")

# Load data
synth = pd.read_csv("synthetic_cosmos_final/synthetic_cosmic_catalog_calibrated.csv")
real1 = pd.concat([chunk for chunk in pd.read_csv("JApJ94494_2MASS_GAIADR3_EPOCH.csv", chunksize=int(20000), low_memory=False)], ignore_index=True)
real2 = pd.concat([chunk for chunk in pd.read_csv("DESIDR8_SDSSDR16_SIMBAD.csv", chunksize=int(20000), low_memory=False)], ignore_index=True)

# Your thesis metrics function
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
        df['T_cosmo'] = 1.0
    if 'Vcmb' in df.columns:
        df['Tully_Fisher'] = df.get('gmag', 0) + 5 * np.log10(df['Vcmb'] / 100.0)
    else:
        df['Tully_Fisher'] = df.get('gmag', 0)
    df['Anthropic'] = 0.0  # will be overwritten with independent local version
    for col in ['flux_gr', 'pm_mag_proxy', 'mag_ratio', 'T_cosmo', 'Tully_Fisher']:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0).astype(float)
    return df

synth = add_thesis_features(synth)
real1 = add_thesis_features(real1)
real2 = add_thesis_features(real2)

# Full persistent homology + local Betti per galaxy
def add_full_persistence(df, name, ra_col, de_col, z_col, k=25):
    coords = df[[ra_col, de_col, z_col]].dropna().values
    if len(coords) == 0:
        for i in range(3):
            df[name + f'_local_betti_{i}'] = 0
        df[name + '_avg_lifetime'] = 0
        df[name + '_max_lifetime'] = 0
        df[name + '_persistence_entropy'] = 0
        return df

    nn = NearestNeighbors(n_neighbors=k).fit(coords)
    distances, indices = nn.kneighbors(coords)

    # Independent Anthropic from local density
    df[name + '_local_density'] = distances.mean(axis=1)
    df['Anthropic'] = np.abs(df[name + '_local_density'] - np.median(df[name + '_local_density']))

    # Local Betti + persistence features per galaxy
    local_betti = np.zeros((len(coords), 3), dtype=int)
    avg_lifetime = np.zeros(len(coords))
    max_lifetime = np.zeros(len(coords))
    persistence_entropy = np.zeros(len(coords))

    for i in range(len(coords)):
        neigh_idx = indices[i]
        neigh_points = coords[neigh_idx]
        rips = gudhi.RipsComplex(points=neigh_points, max_edge_length=1.0)
        st = rips.create_simplex_tree(max_dimension=2)
        st.compute_persistence()
        betti = st.betti_numbers()
        for j in range(3):
            local_betti[i, j] = betti[j] if len(betti) > j else 0

        # H1 lifetimes
        h1_lifetimes = [d - b for (dim, (b, d)) in st.persistence() if dim == 1 and d < np.inf]
        if h1_lifetimes:
            avg_lifetime[i] = np.mean(h1_lifetimes)
            max_lifetime[i] = np.max(h1_lifetimes)
            persistence_entropy[i] = -np.sum(np.array(h1_lifetimes) * np.log(np.array(h1_lifetimes) + 1e-10))

    for i in range(3):
        df[name + f'_local_betti_{i}'] = local_betti[:, i]
    df[name + '_avg_lifetime'] = avg_lifetime
    df[name + '_max_lifetime'] = max_lifetime
    df[name + '_persistence_entropy'] = persistence_entropy
    print(f"   {name} full persistence + local Betti_0/1/2 computed for all galaxies")
    return df

print("\nComputing full persistence + local Betti...")
real1 = add_full_persistence(real1, "real1", "RAJ2000", "DEJ2000", "Vcmb")
real2 = add_full_persistence(real2, "real2", "RAdeg", "DEdeg", "zphot")
synth = add_full_persistence(synth, "synth", "synthetic_RA", "synthetic_DE", "synthetic_z")

feature_cols = ['flux_gr', 'pm_mag_proxy', 'mag_ratio', 'T_cosmo', 'Tully_Fisher', 'Anthropic']

# Targets (now truly varying local Betti_1)
synth_y = synth['exact_rank']
real1_y = real1['real1_local_betti_1']
real2_y = real2['real2_local_betti_1']

# 5-fold CV
def run_cv(df, y, name):
    X = df[feature_cols].copy()
    kf = KFold(n_splits=5, shuffle=True, random_state=42)
    r2_scores, mse_scores = [], []
    for train_idx, test_idx in kf.split(X):
        X_train, X_test = X.iloc[train_idx], X.iloc[test_idx]
        y_train, y_test = y.iloc[train_idx], y.iloc[test_idx]
        xgb = XGBRegressor(n_estimators=200, learning_rate=0.03, max_depth=6, random_state=42)
        xgb.fit(X_train, y_train)
        y_pred = xgb.predict(X_test)
        r2_scores.append(r2_score(y_test, y_pred))
        mse_scores.append(mean_squared_error(y_test, y_pred))
    print(f"\n{name} — 5-Fold CV (Full Persistence + Local Betti)")
    print(f"   R²  = {np.mean(r2_scores):.4f} ± {np.std(r2_scores):.4f}")
    print(f"   MSE = {np.mean(mse_scores):.4f} ± {np.std(mse_scores):.4f}")
    return np.mean(r2_scores), np.mean(mse_scores)

print("\nRunning 5-fold CV...")
r2_synth, mse_synth = run_cv(synth, synth_y, "Synthetic")
r2_real1, mse_real1 = run_cv(real1, real1_y, "Real1 JApJ")
r2_real2, mse_real2 = run_cv(real2, real2_y, "Real2 DESI/SDSS")

# PySR + outputs
print("\nRunning PySR on synthetic...")
from pysr import PySRRegressor
pysr = PySRRegressor(niterations=80, maxsize=12, random_state=42)
pysr.fit(synth[feature_cols], synth_y)
pysr.get_hall_of_fame().to_csv("hall_of_fame_final.csv", index=False)
print(" hall_of_fame_final.csv saved")

xgb = XGBRegressor(n_estimators=200, learning_rate=0.03, max_depth=6, random_state=42)
xgb.fit(synth[feature_cols], synth_y)
imp = pd.DataFrame({'feature': feature_cols, 'importance': xgb.feature_importances_}).sort_values('importance', ascending=False)
imp.to_csv("feature_importance.csv", index=False)
print(" feature_importance.csv saved")

pred_df = pd.DataFrame({
    'true_target': synth['exact_rank'],
    'flux_gr': synth['flux_gr'],
    'pm_mag_proxy': synth['pm_mag_proxy'],
    'mag_ratio': synth['mag_ratio']
})
pred_df.to_csv("predictions_final.csv", index=False)
print(" predictions_final.csv saved")

print("\n Processing Complete — Full Persistent Homology + Local Betti per Galaxy")
