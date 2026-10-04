import pandas as pd
import numpy as np
from sklearn.model_selection import KFold
from xgboost import XGBRegressor
from sklearn.metrics import r2_score, mean_squared_error
from sklearn.neighbors import NearestNeighbors
import gudhi
import warnings
warnings.filterwarnings('ignore')


print("🚀 Step 11 — Lagrangian 3-Body Proxy + Full Local Betti_0/1/2 (no leakage)")


# Load data
synth = pd.read_csv("synthetic_cosmos_final/synthetic_cosmic_catalog_calibrated.csv")
real1 = pd.concat([chunk for chunk in pd.read_csv("JApJ94494_2MASS_GAIADR3_EPOCH.csv", chunksize=20000, low_memory=False)], ignore_index=True)
real2 = pd.concat([chunk for chunk in pd.read_csv("DESIDR8_SDSSDR16_SIMBAD.csv", chunksize=20000, low_memory=False)], ignore_index=True)


# Leakage-free photometric features
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


# Local Betti_0/1/2 + Lagrangian 3-body proxy
def add_local_topology(df, name, ra_col, de_col, z_col, k=20, subsample=10000):
    coords = df[[ra_col, de_col, z_col]].dropna().values
    if len(coords) == 0:
        for i in range(3):
            df[name + f'_local_betti_{i}'] = 0
        df[name + '_local_density'] = 0
        df[name + '_3body_proxy'] = 0
        return df


    nn = NearestNeighbors(n_neighbors=k).fit(coords)
    distances, indices = nn.kneighbors(coords)


    # Local density and 3-body proxy
    df[name + '_local_density'] = distances.mean(axis=1)
    # Lagrangian 3-body proxy: simple pairwise potential for the 3 nearest neighbors (magnitude as mass proxy)
    three_body = np.zeros(len(coords))
    for i in range(len(coords)):
        neigh_idx = indices[i][:3]
        neigh_coords = coords[neigh_idx]
        neigh_mag = df.iloc[neigh_idx]['mag_ratio'].values if 'mag_ratio' in df.columns else np.ones(3)
        # Approximate -G m_i m_j / r_ij for the three pairs
        r12 = np.linalg.norm(neigh_coords[0] - neigh_coords[1])
        r13 = np.linalg.norm(neigh_coords[0] - neigh_coords[2])
        r23 = np.linalg.norm(neigh_coords[1] - neigh_coords[2])
        m1, m2, m3 = neigh_mag
        proxy = -(m1*m2/r12 + m1*m3/r13 + m2*m3/r23) if r12 > 0 and r13 > 0 and r23 > 0 else 0
        three_body[i] = proxy
    df[name + '_3body_proxy'] = three_body
    print(f"   {name} local density + 3-body proxy computed")


    # Local Betti on subsample
    subsample_idx = np.random.choice(len(coords), min(int(subsample), len(coords)), replace=False)
    for i in subsample_idx:
        neigh_idx = indices[i]
        neigh_points = coords[neigh_idx]
        rips = gudhi.RipsComplex(points=neigh_points, max_edge_length=1.0)
        st = rips.create_simplex_tree(max_dimension=2)
        st.compute_persistence()
        betti = st.betti_numbers()
        for j in range(3):
