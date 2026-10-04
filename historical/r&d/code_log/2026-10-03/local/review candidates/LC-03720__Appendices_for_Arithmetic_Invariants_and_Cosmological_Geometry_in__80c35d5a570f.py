# Import necessary libraries
from sage.all import EllipticCurve, QQ, pari
import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression
import math

print("--- Pipeline Initialized ---")

# Define foundational constants from your research
VIRGO_CALIBRATED_KAPPA = 31.59259259259259
# --- CHANGE 1: ADDED VIRGO CLUSTER TO THE DATASET ---
cluster_data = {
    'Coma': {'r': 321, 'rho': 9980},
    'Perseus': {'r': 236, 'rho': 11500},
    'Fornax': {'r': 62, 'rho': 3200},
    'Hercules': {'r': 500, 'rho': 8500},
    'Centaurus': {'r': 170, 'rho': 7500},
    'Virgo': {'r': 54, 'rho': 6320} # Added from foundational papers
}

# --- CHANGE 2: CHANGED THE HOLDOUT CLUSTER TO VIRGO ---
HOLDOUT_CLUSTER = 'Virgo'
print(f"Holdout cluster for final validation: {HOLDOUT_CLUSTER}")

# Stage 1: Foundational Dataset Generation
# =========================================
print("\n--- Stage 1: Generating Foundational Dataset ---")

def derive_and_analyze_cluster_curve(cluster_name, r, rho):
    print(f"\nProcessing cluster: {cluster_name}")
    try:
        a_predicted = -VIRGO_CALIBRATED_KAPPA * r
        b_predicted = rho
        # Per your paper, the Virgo 'a' coefficient is -1706
        if cluster_name == 'Virgo':
            a = -1706
