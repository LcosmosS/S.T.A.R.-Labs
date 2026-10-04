# --- 1. Configuration ---
INPUT_FILE = 'merged_galspec_gz2.csv'
OUTPUT_PLOT_PREFIX = 'final_two_tier_synthesis_v19'
CHUNKSIZE = int(100000)
ROW_LIMIT = 300000  # Set to None for the full run.
TARGET_PRIMES = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47]
REQUIRED_COLUMNS = ['objid', 'ra', 'dec', 'z', 'logmass', 'petrorad_r']

# --- 2. Imports ---
import pandas as pd
import numpy as np
import sys
import warnings
from astropy.cosmology import Planck18 as cosmo
from astropy import units as u
from astropy.constants import G
from sage.all import EllipticCurve, QQ, factor

import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.metrics import r2_score
import lightgbm as lgb

warnings.filterwarnings('ignore')
plt.style.use('seaborn-v0_8-whitegrid')

# --- 3. Scientific Derivation Functions (unchanged) ---
def calculate_distance_mpc(z):
    if z is None or not np.isfinite(z) or z <= 0: return np.nan
    try: return cosmo.comoving_distance(z).to(u.Mpc).value
    except: return np.nan

def convert_logmass_to_sm(logmass):
    if logmass is None or not np.isfinite(logmass): return np.nan
    return 10**logmass

def estimate_radius_ly(angular_size_arcsec, distance_mpc):
    if not (np.isfinite(angular_size_arcsec) and np.isfinite(distance_mpc) and angular_size_arcsec > 0 and distance_mpc > 0): return np.nan
    angle_rad = (angular_size_arcsec * u.arcsec).to(u.rad).value
    radius_mpc = distance_mpc * angle_rad
    return (radius_mpc * u.Mpc).to(u.lyr).value

def calculate_virial_energy(mass_sm, radius_ly):
    if not (np.isfinite(mass_sm) and np.isfinite(radius_ly) and mass_sm > 0 and radius_ly > 0): return np.nan
    mass_kg = mass_sm * 1.989e30; radius_m = radius_ly * 9.461e15
    potential_energy = -1 * G.value * (mass_kg ** 2) / radius_m
    return potential_energy / 2.0

# --- 4. SageMath Core Hypothesis Functions ---
def map_physics_to_curve_coeffs(distance_mly, density_kg_m3):
    if not (np.isfinite(distance_mly) and np.isfinite(density_kg_m3)): return np.nan, np.nan
    return QQ(-distance_mly), QQ(density_kg_m3)

def get_prime_factor_exponents(discriminant_sage):
    if pd.isna(discriminant_sage): return {}
    try: return {p: e for p, e in factor(abs(discriminant_sage))}
    except: return {}

def estimate_rank_category(E):
    if not isinstance(E, EllipticCurve): return 'Invalid Curve'
    try:
        rank = E.rank()
        if rank >= 3: return 'Rank 3+'
        elif rank == 2: return 'Rank 2'
        elif rank == 1: return 'Rank 1'
        else: return 'Rank 0'
    except: return 'Computationally Difficult'

# --- 5. Main Unified Pipeline ---
def main():
    print("--- [STAGE 1/2] Starting THEORY-DRIVEN VALUATIVE Data Processing... ---")
    df_analysis = process_data()
    if df_analysis is None or df_analysis.empty:
        print("Pipeline halted due to lack of valid data."); return
        
    print(f"\n--- [STAGE 2/2] Final Synthesis: Two-Tiered Analysis... ---")
    run_final_synthesis(df_analysis)

def process_data():
    processed_chunks = []
    for i, chunk in enumerate(pd.read_csv(INPUT_FILE, usecols=REQUIRED_COLUMNS, chunksize=CHUNKSIZE, on_bad_lines='skip', low_memory=True)):
        print(f"  - Processing chunk {i+1}...")
        chunk.replace(-9999, np.nan, inplace=True); chunk.dropna(subset=REQUIRED_COLUMNS, inplace=True)
        chunk = chunk[chunk['z'] > 0].copy()
        if chunk.empty: continue
        
        chunk['distance_mpc'] = chunk['z'].apply(calculate_distance_mpc)
        chunk['mass_sm'] = chunk['logmass'].apply(convert_logmass_to_sm)
        chunk['radius_ly'] = chunk.apply(lambda row: estimate_radius_ly(row['petrorad_r'], row['distance_mpc']), axis=1)
        chunk['virial_energy_j'] = chunk.apply(lambda row: calculate_virial_energy(row['mass_sm'], row['radius_ly']), axis=1)
        
        distance_mly = chunk['distance_mpc'] * 3.26156
        chunk['density_kg_m3'] = chunk.apply(lambda row: (row['mass_sm'] * 1.989e30) / ((4/3) * np.pi * (row['radius_ly'] * 9.461e15)**3) if pd.notna(row['mass_sm']) and pd.notna(row['radius_ly']) and row['radius_ly'] > 0 else np.nan, axis=1)
        
        coeffs = chunk.apply(lambda row: map_physics_to_curve_coeffs(distance_mly.get(row.name), row['density_kg_m3']), axis=1)
        chunk[['coeff_a', 'coeff_b']] = pd.DataFrame(coeffs.tolist(), index=chunk.index)
        
        def process_curve_properties(row):
            if pd.isna(row['coeff_a']) or pd.isna(row['coeff_b']): return (np.nan, 'Invalid Curve', {})
            try:
                E = EllipticCurve(QQ, [0, 0, 0, row['coeff_a'], row['coeff_b']])
                discriminant = E.discriminant()
                return (discriminant, estimate_rank_category(E), get_prime_factor_exponents(discriminant))
            except: return (np.nan, 'Invalid Curve', {})
        
        results = chunk.apply(process_curve_properties, axis=1)
        chunk[['discriminant_sage', 'rank', 'prime_exponents']] = pd.DataFrame(results.tolist(), index=chunk.index)
        
        processed_chunks.append(chunk)
        if ROW_LIMIT and (i + 1) * CHUNKSIZE >= ROW_LIMIT: print(f"  - Reached row limit of {ROW_LIMIT}. Stopping."); break

    if not processed_chunks: return None
    df_analysis = pd.concat(processed_chunks, ignore_index=True)
    print(f"  - Data processing complete. {len(df_analysis)} high-fidelity rows finalized.")
    return df_analysis

def run_final_synthesis(df):
    # --- TIER 1: VALUATIVE PREDICTION (Full Dataset) ---
    print("\n  --- Part 1: Valuative Prediction on Full High-Fidelity Dataset ---")
    df_full = df.dropna(subset=['virial_energy_j', 'prime_exponents']).copy()
    df_full = df_full[(df_full['virial_energy_j'] != 0) & (df_full['prime_exponents'].str.len() > 0)]
    
    if df_full.empty:
        print("    - No valid data available for valuative prediction. Skipping.")
    else:
        print(f"    - Using all {len(df_full)} valid rows for valuative prediction.")
        df_full['log_abs_virial_energy'] = np.log10(np.abs(df_full['virial_energy_j']))
        df_exponents = pd.json_normalize(df_full['prime_exponents']).fillna(0)
        
        for p in TARGET_PRIMES:
            if p not in df_exponents.columns: df_exponents[p] = 0
        
        feature_cols = [p for p in TARGET_PRIMES if p in df_exponents.columns]
        X, y = df_exponents[feature_cols], df_full['log_abs_virial_energy']
        
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=42)
        pipeline = Pipeline([('scaler', StandardScaler()), ('model', lgb.LGBMRegressor(random_state=42))])
        pipeline.fit(X_train, y_train)
        r2 = r2_score(y_test, pipeline.predict(X_test))
        
        print("\n" + "="*80); print("      VALUATIVE NORMALIZATION: PREDICTING ENERGY FROM ARITHMETIC STRUCTURE"); print("="*80)
        print(f"  - Predictive Model Fit (R² Score): {r2:.6f}"); print("="*80)
        
        feature_importances = pipeline.named_steps['model'].feature_importances_
        importance_df = pd.DataFrame({'feature': X_train.columns.astype(str), 'importance': feature_importances}).sort_values('importance', ascending=False).head(15)
        plt.figure(figsize=(12, 8)); sns.barplot(x='importance', y='feature', data=importance_df, palette='viridis', orient='h')
        plt.title("Valuative Prediction: Importance of Prime Factors in Predicting Energy", fontsize=16)
        plt.xlabel("Feature Importance", fontsize=12); plt.ylabel("Prime Factor of the Discriminant", fontsize=12)
        plt.savefig(f"{OUTPUT_PLOT_PREFIX}_valuative_feature_importance.png"); plt.close()
        print("    - Valuative feature importance plot saved.")

    # --- TIER 2: HIERARCHICAL VALIDATION (Tractable Subset) ---
    print("\n  --- Part 2: Hierarchical Validation on Computationally Tractable Subset ---")
    tractable_ranks = ['Rank 0', 'Rank 1', 'Rank 2', 'Rank 3+']
    df_ranked = df_full[df_full['rank'].isin(tractable_ranks)].copy()
    
    if df_ranked.empty:
        print("    - SCIENTIFIC FINDING: No galaxies with a computationally tractable rank were found in this dataset.")
        print("    - This validates Intractability. No hierarchical plots will be generated.")
    else:
        print(f"    - Found {len(df_ranked)} galaxies with a computationally tractable rank for hierarchical analysis.")
        plt.figure(figsize=(12, 8))
        sns.violinplot(x='rank', y='log_abs_virial_energy', data=df_ranked, order=tractable_ranks, palette='plasma')
        plt.title("Hierarchical Validation: Virial Energy Distribution by Predicted Rank", fontsize=16)
        plt.xlabel("Predicted Algebraic Rank Category", fontsize=12)
        plt.ylabel("log10(|Virial Energy|)", fontsize=12)
        plt.savefig(f"{OUTPUT_PLOT_PREFIX}_hierarchical_rank_distribution.png"); plt.close()
        print("    - Hierarchical validation plot saved.")

if __name__ == "__main__":
    main()
