# ============================================================
#  ACSC Empirical Verification Notebook
#  Author: Patrick J. McNamara
#  Purpose: Reproducible implementation of the ACSC falsification protocol
# ============================================================

import pandas as pd
import numpy as np
import gudhi
from sage import *
from scipy.stats import wasserstein_distance
import matplotlib.pyplot as plt

# ============================================================
# 1. Load Arithmetic Invariants
# ============================================================

CSV_PATH = "arithmetic_invariants.csv"

try:
    df = pd.read_csv(CSV_PATH)
    print(f"Loaded {len(df)} elliptic curves.")
except FileNotFoundError:
    raise FileNotFoundError("CSV not found. Place arithmetic_invariants.csv in the working directory.")

df.head()

# ============================================================
# 2. Projection Map Φ
# ============================================================

class ProjectionPhi:
    def __init__(self, delta_max, n_max, alpha=1.0):
        self.delta_max = delta_max
        self.n_max = n_max
        self.alpha = alpha

    def project(self, df):
        phi = (np.log(df['delta']) / np.log(self.delta_max)) * 2 * np.pi
        theta = (np.log(df['conductor']) / np.log(self.n_max)) * np.pi
        z = self.alpha * df['rank']

        rho = df['regulator'] + z

        x = rho * np.cos(theta) * np.cos(phi)
        y = rho * np.cos(theta) * np.sin(phi)

        return np.vstack([x, y, z]).T

phi_map = ProjectionPhi(delta_max=1e12, n_max=1e6, alpha=1.0)
arith_pc = phi_map.project(df)
arith_pc[:5]

# ============================================================
# 3. Persistence Computation
# ============================================================

def compute_persistence(point_cloud, max_edge_length=50.0):
    rc = gudhi.RipsComplex(points=point_cloud, max_edge_length=max_edge_length)
    st = rc.create_simplex_tree(max_dimension=2)
    return st.persistence()

arith_pd = compute_persistence(arith_pc)
arith_pd[:10]

# ============================================================
# 4. Load Cosmic Data
# ============================================================

COSMIC_PATH = "synthetic_cosmic_catalog.csv"
cosmo_df = pd.read_csv(COSMIC_PATH)
cosmo_pc = cosmo_df[['x','y','z']].values

cosmo_pd = compute_persistence(cosmo_pc)

# ============================================================
# 5. Wasserstein Distance
# ============================================================

def extract_dim(diag, dim):
    return np.array([p[1] for p in diag if p[0] == dim])

arith_1 = extract_dim(arith_pd, 1)
cosmo_1 = extract_dim(cosmo_pd, 1)

W2 = gudhi.wasserstein_distance(arith_1, cosmo_1, order=2.0)
print("W2 (Betti-1):", W2)

# ============================================================
# 6. Null Model Falsification
# ============================================================

def falsification_test(arith_pc, cosmo_pc, n_perm=50):
    diag_arith = compute_persistence(arith_pc)
    diag_cosmo = compute_persistence(cosmo_pc)
    obs = gudhi.wasserstein_distance(
        extract_dim(diag_arith, 1),
        extract_dim(diag_cosmo, 1),
        order=2.0
    )

    nulls = []
    for _ in range(n_perm):
        perm = arith_pc.copy()
        np.random.shuffle(perm[:,2])
        diag_null = compute_persistence(perm)
        w = gudhi.wasserstein_distance(
            extract_dim(diag_null, 1),
            extract_dim(diag_cosmo, 1),
            order=2.0
        )
        nulls.append(w)

    p_value = np.mean(np.array(nulls) <= obs)
    return obs, p_value

obs, p = falsification_test(arith_pc, cosmo_pc)
print("Observed W2:", obs)
print("p-value:", p)

