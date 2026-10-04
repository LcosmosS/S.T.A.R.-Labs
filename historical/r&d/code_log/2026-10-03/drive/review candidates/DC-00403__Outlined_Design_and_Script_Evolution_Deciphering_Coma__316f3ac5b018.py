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




# Stage 1: Foundational Dataset Generation
# =========================================
print("\n--- Stage 1: Generating Foundational Dataset ---")


def derive_and_analyze_cluster_curve(cluster_name, r, rho):
    print(f"\nProcessing cluster: {cluster_name}")
    try:
        a_predicted = -VIRGO_CALIBRATED_KAPPA * r
        b_predicted = rho
        if cluster_name == 'Virgo':
            a = -1706
        else:
            a = round(a_predicted)
        b = b_predicted
        print(f"  Derived curve: y^2 = x^3 + {a}x + {b}")
        
        E_sage = EllipticCurve(QQ, [a, b])
        
        try:
            rank = E_sage.rank(algorithm='pari')
        except RuntimeError as e:
            print(f"  SKIPPED: Rank computation failed with error: {e}")
            return None


        if rank == 1:
            generator = E_sage.gens()[0]
            print(f"  SUCCESS: Rank 1 curve found.")
            print(f"  Generator: {generator}")
            return {'cluster': cluster_name, 'r': r, 'rho': rho, 'a': a, 'b': b, 'rank': rank, 'generator': generator, 'curve_obj': E_sage}
        else:
            print(f"  SKIPPED: Predicted rank is {rank}, not 1.")
            return None
            
    except (SignalError, TypeError, ValueError) as e:
