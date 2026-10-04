# --- CHANGE: REMOVED 'RuntimeError' FROM THE SAGE IMPORT, KEPT 'SignalError' ---
from sage.all import EllipticCurve, QQ, pari, Integer, SignalError
import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression
import math

print("--- Pipeline Initialized ---")

VIRGO_CALIBRATED_KAPPA = 31.59259259259259

cluster_data = {
    'Coma': {'r': 321, 'rho': 9980},
    'Perseus': {'r': 236, 'rho': 11500},
    'Centaurus': {'r': 170, 'rho': 7500},
    'Virgo': {'r': 54, 'rho': 6320},
    'Hydra': {'r': 190, 'rho': 9000},
    'Leo': {'r': 330, 'rho': 8000},
    'Pavo-Indus': {'r': 230, 'rho': 10500},
    'Shapley': {'r': 650, 'rho': 18000},
    'Ursa Major': {'r': 60, 'rho': 2500},
    'Horologium': {'r': 700, 'rho': 12000},
    'Fornax': {'r': 62, 'rho': 3200},
    'Hercules': {'r': 500, 'rho': 8500}
}

HOLDOUT_CLUSTER = 'Shapley'
print(f"Holdout cluster for final validation: {HOLDOUT_CLUSTER}")
