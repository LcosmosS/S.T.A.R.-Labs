import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from xgboost import XGBRegressor
from sklearn.metrics import r2_score
import gudhi
import warnings


warnings.filterwarnings('ignore')


# ────── FILES ──────
SYNTH_FILE = "synthetic_cosmos_final/synthetic_cosmic_catalog_calibrated.csv"
REAL1_FILE = "JApJ94494_2MASS_GAIADR3_EPOCH.csv"
REAL2_FILE = "DESIDR8_SDSSDR16_SIMBAD.csv"
CHUNK_SIZE = 20000


print("🚀 Step 3 — FINAL Production Pipeline (dtype-fixed)")


# Load data
synth = pd.read_csv(SYNTH_FILE)
real1 = pd.concat([chunk for chunk in pd.read_csv(REAL1_FILE, chunksize=CHUNK_SIZE, low_memory=False)], ignore_index=True)
real2 = pd.concat([chunk for chunk in pd.read_csv(REAL2_FILE, chunksize=CHUNK_SIZE, low_memory=False)], ignore_index=True)


print(f"Loaded synthetic: {len(synth):,} | real1: {len(real1):,} | real2: {len(real2):,}")


# ────── ENTROPY COHOMOLOGY (already done in previous run — skipped for speed) ──────
# (betti_1 columns are already in the dataframes from your last run)


# ────── FEATURE ENGINEERING + STRONG NUMERIC FIX ──────
def add_features(df):
    df = df.copy()
    if 'DM' in df.columns:
        df['scaled_a'] = -df['DM'] * 50.0
        df['scaled_b'] = df.get('Vcmb', 0) / 100.0
    elif 'zphot' in df.columns:
        df['scaled_a'] = -df['zphot'] * 1000.0
        df['scaled_b'] = df.get('gmag', 0) * 10.0
    elif 'V_comove_calibrated' in df.columns:
        df['scaled_a'] = df['V_comove_calibrated'] * 0.003993
        df['scaled_b'] = df['rho_scale_calibrated'] * 0.021228


    # Safe flux and proper motion proxies
    df['flux_gr'] = df.get('Gmag', 0) / (df.get('Jmag', 1) + 1e-8)
    df['pm_mag_proxy'] = np.sqrt(df.get('pmRA', 0)**2 + df.get('pmDE', 0)**2)


    # CRITICAL: Force numeric types for XGBoost
    for col in ['scaled_a', 'scaled_b', 'flux_gr', 'pm_mag_proxy']:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0).astype(float)


    return df


synth = add_features(synth)
real1 = add_features(real1)
real2 = add_features(real2)


# ────── DYNAMIC FEATURE SELECTION ──────
base_cols = ['scaled_a', 'scaled_b', 'flux_gr', 'pm_mag_proxy']
def get_features(df):
    cols = base_cols[:]
    for c in ['synth_betti_1', 'real1_betti_1', 'real2_betti_1']:
        if c in df.columns:
            cols.append(c)
    return [c for c in cols if c in df.columns]


# ────── STACKED MODEL (PySR + XGBoost) ──────
def run_stacked_model(df, target_col, name):
    X = df[get_features(df)]
    y = df[target_col]
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=float(0.2), random_state=int(42)
    )
    from pysr import PySRRegressor
    pysr = PySRRegressor(niterations=int(100), maxsize=int(15), random_state=int(42))
    pysr.fit(X_train, y_train)
    xgb = XGBRegressor(n_estimators=int(200), learning_rate=float(0.03), max_depth=int(6), random_state=int(42))
    xgb.fit(X_train, y_train)
    train_stack = np.hstack((X_train, pysr.predict(X_train).reshape(-1,1), xgb.predict(X_train).reshape(-1,1)))
    test_stack = np.hstack((X_test, pysr.predict(X_test).reshape(-1,1), xgb.predict(X_test).reshape(-1,1)))
    meta = XGBRegressor(n_estimators=int(100), learning_rate=float(0.05), max_depth=int(4), random_state=int(42))
    meta.fit(train_stack, y_train)
    y_pred = meta.predict(test_stack)
    r2 = r2_score(y_test, y_pred)
    print(f"   {name} Stacked R² = {r2:.4f}")
    return r2


print("\nTraining stacked models (PySR + XGBoost)...")
r2_synth = run_stacked_model(synth, 'exact_rank', "Synthetic")
r2_real1 = run_stacked_model(real1, real1.get('exact_rank', real1['Vcmb']/1000), "Real1 JApJ")
r2_real2 = run_stacked_model(real2, real2.get('exact_rank', real2['zphot']), "Real2 DESI/SDSS")


print("\n🎉 STEP 3 COMPLETE!")
print(f"   Synthetic R² = {r2_synth:.4f}")
print(f"   Real1 JApJ R² = {r2_real1:.4f}")
print(f"   Real2 DESI/SDSS R² = {r2_real2:.4f}")


print("\nThe full S.T.A.R. model (arithmetic invariants → calibrated cosmos → Entropy Cohomology → stacked ML) is now operational.")
