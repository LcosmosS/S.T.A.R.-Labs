# Import necessary libraries
from sage.all import EllipticCurve, QQ, pari
import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression
import math


print("--- Pipeline Initialized ---")


# Define foundational constants from your research
VIRGO_CALIBRATED_KAPPA = 31.59259259259259  


# Define the dataset of galaxy clusters for analysis
cluster_data = {
    'Coma': {'r': 321, 'rho': 9980},
    'Perseus': {'r': 236, 'rho': 11500}, 
    'Fornax': {'r': 62, 'rho': 3200},    
    'Hercules': {'r': 500, 'rho': 8500},
    'Centaurus': {'r': 170, 'rho': 7500}
}


HOLDOUT_CLUSTER = 'Centaurus'
print(f"Holdout cluster for final validation: {HOLDOUT_CLUSTER}")




# Stage 1: Foundational Dataset Generation
# =========================================
# (No changes in this stage)
print("\n--- Stage 1: Generating Foundational Dataset ---")


def derive_and_analyze_cluster_curve(cluster_name, r, rho):
    print(f"\nProcessing cluster: {cluster_name}")
    try:
        a_predicted = -VIRGO_CALIBRATED_KAPPA * r
        b_predicted = rho
        a = round(a_predicted)
        b = b_predicted
        print(f"  Derived curve: y^2 = x^3 + {a}x + {b}")
        E = EllipticCurve(QQ, [a, b])
        rank = E.rank()
        if rank == 1:
            generator = E.gens()[0]
            print(f"  SUCCESS: Rank 1 curve found.")
            print(f"  Generator: {generator}")
            return {'cluster': cluster_name, 'r': r, 'rho': rho, 'a': a, 'b': b, 'rank': rank, 'generator': generator, 'curve_obj': E}
        else:
            print(f"  SKIPPED: Predicted rank is {rank}, not 1.")
            return None
    except Exception as e:
        print(f"  ERROR processing {cluster_name}: {e}")
        return None


analysis_results = []
for name, data in cluster_data.items():
    if name != HOLDOUT_CLUSTER:
        result = derive_and_analyze_cluster_curve(name, data['r'], data['rho'])
        if result:
            analysis_results.append(result)


holdout_result = derive_and_analyze_cluster_curve(HOLDOUT_CLUSTER, cluster_data[HOLDOUT_CLUSTER]['r'], cluster_data[HOLDOUT_CLUSTER]['rho'])
df = pd.DataFrame(analysis_results)


print("\n--- Stage 1 Complete: Foundational Dataset ---")
if not df.empty:
    df['x_coord'] = df['generator'].apply(lambda p: p[0])
    df['y_coord'] = df['generator'].apply(lambda p: p[1])
    df['x_num'] = df['x_coord'].apply(lambda x: x.numerator())
    df['x_den'] = df['x_coord'].apply(lambda x: x.denominator())
    df['y_num'] = df['y_coord'].apply(lambda y: y.numerator())
    df['y_den'] = df['y_coord'].apply(lambda y: y.denominator())
    print("Training Dataset:")
    print(df[['cluster', 'r', 'rho', 'generator']])
else:
    print("Training Dataset is empty.")


if holdout_result is None:
    print(f"\n\033[91mCRITICAL PIPELINE ERROR:\033[0m")
    print(f"The designated holdout cluster, '{HOLDOUT_CLUSTER}', did not produce a valid Rank 1 curve and was skipped.")
    print("The pipeline cannot proceed to the validation stage without a valid holdout case.")
    exit() 


if df.empty:
    print(f"\n\033[91mCRITICAL PIPELINE ERROR:\033[0m")
    print("The training dataset is empty. Cannot proceed to model training.")
    exit()


# Stage 2: Analyzing Denominator Structure
# =========================================


print("\n--- Stage 2: Adaptive Denominator Analysis ---")


# --- MODIFIED THIS ENTIRE FUNCTION TO BE DATA-DRIVEN ---
def find_denominator_rule(denominators_df):
    """
    Analyzes the denominators in the training data to choose a rule.
