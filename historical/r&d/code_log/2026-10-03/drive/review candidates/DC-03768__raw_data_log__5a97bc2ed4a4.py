import pandas as pd
import numpy as np
import warnings
from sage.all import EllipticCurve, QQ, pari, factor
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.impute import KNNImputer
from sklearn.ensemble import RandomForestClassifier
from xgboost import XGBRegressor
from imblearn.over_sampling import SMOTE
import gudhi
import plotly.graph_objects as go
import matplotlib.pyplot as plt
import os


warnings.filterwarnings('ignore')
os.makedirs("star_results", exist_ok=True)
CHUNKSIZE = 50000
INPUT_FILE = 'merged_galspec_gz2.csv'  # or GalSpecExtra.csv


def process_chunk(chunk):
    chunk = chunk.copy()
    chunk.replace(-9999, np.nan, inplace=True)
    key_cols = ['z', 'Fg', 'Fr', 'Fz', 'EBV', 'plx', 'pmRA', 'pmDE', 'Chi2', 'delChi2', 'TSNR2_ELG', 'TSNR2_LRG', 'Morph', 'OType']
    chunk = chunk.dropna(subset=key_cols)
    chunk = chunk[(chunk['Fg'] > 0) & (chunk['Fr'] > 0) & (chunk['Fz'] > 0)]
    
    # Safe feature engineering
    coeff_cols = [col for col in chunk.columns if col.startswith('COEFF')]
    if coeff_cols:
        chunk['coeff_sum'] = chunk[coeff_cols].sum(axis=1)
    chunk['flux_gr'] = chunk['Fg'] / chunk['Fr']
    chunk['flux_rz'] = chunk['Fr'] / chunk['Fz']
    chunk['log_EBV'] = np.log(chunk['EBV'] + 1e-10)
    chunk['pm_mag'] = np.sqrt(chunk['pmRA']**2 + chunk['pmDE']**2)
    chunk['chi_ratio'] = chunk['Chi2'] / (chunk['delChi2'] + 1e-10)
    chunk['tsnr_ratio_elg_lrg'] = chunk['TSNR2_ELG'] / (chunk['TSNR2_LRG'] + 1e-10)
    
    # Clip to prevent overflow
    numeric_cols = chunk.select_dtypes(include=[np.number]).columns
    chunk[numeric_cols] = np.clip(chunk[numeric_cols], -1e12, 1e12)
    
    return chunk


# Load full dataset
df_list = []
for chunk in pd.read_csv(INPUT_FILE, chunksize=CHUNKSIZE):
    processed = process_chunk(chunk)
    if not processed.empty:
        df_list.append(processed)
df = pd.concat(df_list, ignore_index=True)
print(f"Loaded {len(df)} rows")


# Classifiers (exact, no heuristics)
X_clf_cols = ['Fg', 'Fr', 'Fz', 'EBV', 'plx', 'pmRA', 'pmDE', 'flux_gr', 'flux_rz', 'log_EBV', 'pm_mag', 'coeff_sum', 'chi_ratio', 'tsnr_ratio_elg_lrg']
X_clf = df[X_clf_cols].values
imputer = KNNImputer()
X_clf = imputer.fit_transform(X_clf)
y_regime = (df['z'] >= 0.1).astype(int)
clf_regime = RandomForestClassifier(random_state=42)
print("Regime CV accuracy:", cross_val_score(clf_regime, X_clf, y_regime, cv=5).mean())
clf_regime.fit(X_clf, y_regime)
df['predicted_regime'] = clf_regime.predict(X_clf)


# Elliptic curve + exact rank (no heuristic)
def compute_exact_curve(row):
    try:
        a = QQ(-row['logmass'] * 1e6)   # scaled as before
        b = QQ(row['petrorad_r'] * 1e3)
        E = EllipticCurve(QQ, [0, 0, 0, a, b])
        rank = E.rank(algorithm='pari')   # exact
        disc = E.discriminant()
        return rank, float(disc), E.conductor()
    except:
        return np.nan, np.nan, np.nan
