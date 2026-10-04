import pandas as pd
import numpy as np
from sklearn.model_selection import KFold
from xgboost import XGBRegressor
from sklearn.metrics import r2_score, mean_squared_error
from sklearn.neighbors import NearestNeighbors
import gudhi
import warnings
warnings.filterwarnings('ignore')


print("🚀 Step 8 — Enhanced Local Topology (larger Betti subsample + curvature + filament/void proxy)")


# Load data
synth = pd.read_csv("synthetic_cosmos_final/synthetic_cosmic_catalog_calibrated.csv")
real1 = pd.concat([chunk for chunk in pd.read_csv("JApJ94494_2MASS_GAIADR3_EPOCH.csv", chunksize=20000, low_memory=False)], ignore_index=True)
real2 = pd.concat([chunk for chunk in pd.read_csv("DESIDR8_SDSSDR16_SIMBAD.csv", chunksize=20000, low_memory=False)], ignore_index=True)


# Leakage-free photometric features only
def add_photometric_features(df):
    df = df.copy()
    df['flux_gr'] = df.get('Gmag', 0) / (df.get('Jmag', 1) + 1e-8)
    df['pm_mag_proxy'] = np.sqrt(df.get('pmRA', 0)**2 + df.get('pmDE', 0)**2)
    df['mag_ratio'] = df.get('gmag', 0) / (df.get('rmag', 1) + 1e-8)
    for col in ['flux_gr', 'pm_mag_proxy', 'mag_ratio']:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0).astype(float)
    return df


synth = add_photometric_features(synth)
real1 = add_photometric_features(real1)
real2 = add_photometric_features(real2)


feature_cols = ['flux_gr', 'pm_mag_proxy', 'mag_ratio']


# Enhanced local topology (k-NN + larger Betti subsample)
def add_enhanced_topology(df, name, ra_col, de_col, z_col, k=20, betti_subsample=25000):
    coords = df[[ra_col, de_col, z_col]].dropna().values
    if len(coords) == 0:
        df[name + '_local_density'] = 0
        df[name + '_local_curvature'] = 0
        df[name + '_filament_proxy'] = 0
        df[name + '_local_betti_1'] = 0
        return df


    # k-NN for density, curvature, filament proxy
    nn = NearestNeighbors(n_neighbors=k).fit(coords)
    distances, _ = nn.kneighbors(coords)
    df[name + '_local_density'] = distances.mean(axis=1)                     # local density
    df[name + '_local_curvature'] = distances.std(axis=1)                    # local curvature
    # Filament/void proxy (high density + low anisotropy → filament)
    df[name + '_filament_proxy'] = df[name + '_local_density'] * (1 - distances.std(axis=1)/distances.mean(axis=1))
    print(f"   {name} local density/curvature/filament proxies computed")


    # Larger subsample for local Betti_1
    subsample_idx = np.random.choice(len(coords), min(int(betti_subsample), len(coords)), replace=False)
    subsample = coords[subsample_idx]
    rips = gudhi.RipsComplex(points=subsample, max_edge_length=1.0)
    st = rips.create_simplex_tree(max_dimension=2)
    st.compute_persistence()
    betti = st.betti_numbers()
    local_betti = betti[1] if len(betti) > 1 else 0
    df[name + '_local_betti_1'] = local_betti
    print(f"   {name} local Betti_1 computed on {len(subsample)} points (value = {local_betti})")
    return df


print("\nComputing enhanced local topology...")
real1 = add_enhanced_topology(real1, "real1", "RAJ2000", "DEJ2000", "Vcmb")
real2 = add_enhanced_topology(real2, "real2", "RAdeg", "DEdeg", "zphot")


# Targets (true topological, per-galaxy)
synth_y = synth['exact_rank']
real1_y = real1['real1_local_density']
real2_y = real2['real2_local_density']


# 5-fold CV
def run_cv(X, y, name):
    X = X[feature_cols].copy()
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
    print(f"\n{name} — 5-Fold CV (Enhanced Local Topology)")
    print(f"   R²  = {np.mean(r2_scores):.4f} ± {np.std(r2_scores):.4f}")
    print(f"   MSE = {np.mean(mse_scores):.4f} ± {np.std(mse_scores):.4f}")
    return np.mean(r2_scores), np.mean(mse_scores)


print("\nRunning 5-fold CV...")
r2_synth, mse_synth = run_cv(synth, synth_y, "Synthetic")
r2_real1, mse_real1 = run_cv(real1, real1_y, "Real1 JApJ")
r2_real2, mse_real2 = run_cv(real2, real2_y, "Real2 DESI/SDSS")


# PySR + outputs on synthetic
print("\nRunning PySR on synthetic...")
from pysr import PySRRegressor
pysr = PySRRegressor(niterations=80, maxsize=12, random_state=42)
pysr.fit(synth[feature_cols], synth_y)
pysr.get_hall_of_fame().to_csv("hall_of_fame_final.csv", index=False)
print("✅ hall_of_fame_final.csv saved")


xgb = XGBRegressor(n_estimators=200, learning_rate=0.03, max_depth=6, random_state=42)
xgb.fit(synth[feature_cols], synth_y)
imp = pd.DataFrame({'feature': feature_cols, 'importance': xgb.feature_importances_}).sort_values('importance', ascending=False)
imp.to_csv("feature_importance.csv", index=False)
print("✅ feature_importance.csv saved")


pred_df = pd.DataFrame({
    'true_target': synth['exact_rank'],
    'flux_gr': synth['flux_gr'],
    'pm_mag_proxy': synth['pm_mag_proxy'],
    'mag_ratio': synth['mag_ratio']
})
pred_df.to_csv("predictions_final.csv", index=False)
print("✅ predictions_final.csv saved")


print("\n🎉 Step 8 Complete — Enhanced Local Topology Pipeline")
print("Reply with **analyze step 8** for full interpretation of the new scores.")
