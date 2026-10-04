# --- 1. Configuration ---
INPUT_FILE = 'merged_galspec_gz2.csv'
OUTPUT_PLOT_PREFIX = 'predictive_analysis_v12'
CHUNKSIZE = 100000
ROW_LIMIT = 300000  # Set to None for the full run.
REQUIRED_COLUMNS = ['objid', 'ra', 'dec', 'z', 'logmass', 'petrorad_r']


# --- 2. Imports ---
import pandas as pd
import numpy as np
import sys
import warnings
from astropy.cosmology import Planck18 as cosmo
from astropy import units as u
from astropy.constants import G
from sage.all import EllipticCurve, QQ


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


# --- 4. SageMath Core Hypothesis Functions (unchanged) ---
def map_physics_to_curve_coeffs(distance_mly, density_kg_m3):
    if not (np.isfinite(distance_mly) and np.isfinite(density_kg_m3)): return np.nan, np.nan
    return QQ(-distance_mly), QQ(density_kg_m3)


# --- 5. Main Unified Pipeline ---
def main():
    print("--- [STAGE 1/4] Starting HIGH-FIDELITY Data Processing... ---")
    df_analysis = process_data()
    if df_analysis is None or df_analysis.empty:
        print("Pipeline halted due to lack of valid data."); return
        
    print(f"\n--- [STAGE 2/4] Full-Population Exploratory Analysis... ---")
    df_clean = clean_and_prepare_data(df_analysis)
    run_exploratory_analysis(df_clean)


    print(f"\n--- [STAGE 3/4] Predictive Modeling with 75/25 Split... ---")
    run_predictive_modeling(df_clean)


    print(f"\nDefinitive predictive analysis complete. All plots saved with prefix '{OUTPUT_PLOT_PREFIX}_*'")


def process_data():
    processed_chunks = []
    total_rows_processed = 0
    try:
        chunk_iter = pd.read_csv(INPUT_FILE, usecols=REQUIRED_COLUMNS, chunksize=CHUNKSIZE, on_bad_lines='skip', low_memory=True)
    except (FileNotFoundError, ValueError) as e:
        print(f"Error reading input file: {e}", file=sys.stderr); return None
    
    for i, chunk in enumerate(chunk_iter):
        print(f"  - Processing chunk {i+1}...")
        chunk.replace(-9999, np.nan, inplace=True)
        chunk.dropna(subset=REQUIRED_COLUMNS, inplace=True)
        chunk = chunk[chunk['z'] > 0].copy()
        if chunk.empty: continue
        
        chunk['distance_mpc'] = chunk['z'].apply(calculate_distance_mpc)
        chunk['mass_sm'] = chunk['logmass'].apply(convert_logmass_to_sm)
        chunk['radius_ly'] = chunk.apply(lambda row: estimate_radius_ly(row['petrorad_r'], row['distance_mpc']), axis=1)
        chunk['virial_energy_j'] = chunk.apply(lambda row: calculate_virial_energy(row['mass_sm'], row['radius_ly']), axis=1)
        
        valid_data = chunk['radius_ly'].notna() & (chunk['radius_ly'] > 0) & chunk['mass_sm'].notna()
        radius_m = chunk.loc[valid_data, 'radius_ly'] * 9.461e15
        mass_kg = chunk.loc[valid_data, 'mass_sm'] * 1.989e30
        volume_m3 = (4/3) * np.pi * (radius_m ** 3)
        chunk.loc[valid_data, 'density_kg_m3'] = mass_kg / volume_m3
        
        distance_mly = chunk['distance_mpc'] * 3.26156
        coeffs = chunk.apply(lambda row: map_physics_to_curve_coeffs(distance_mly.get(row.name), row['density_kg_m3']), axis=1)
        chunk[['coeff_a', 'coeff_b']] = pd.DataFrame(coeffs.tolist(), index=chunk.index)
        
        def process_curve(row):
            if pd.isna(row['coeff_a']) or pd.isna(row['coeff_b']): return np.nan
            try: return EllipticCurve(QQ, [0, 0, 0, row['coeff_a'], row['coeff_b']]).discriminant()
            except: return np.nan
        
        chunk['discriminant'] = chunk.apply(process_curve, axis=1)
        chunk['discriminant'] = pd.to_numeric(chunk['discriminant'], errors='coerce')
        
        processed_chunks.append(chunk)
        total_rows_processed += len(chunk)
        
        if ROW_LIMIT and total_rows_processed >= ROW_LIMIT:
            print(f"  - Reached row limit of {ROW_LIMIT}. Stopping."); break


    if not processed_chunks: return None
    df_analysis = pd.concat(processed_chunks, ignore_index=True)
    print(f"  - Data processing complete. {len(df_analysis)} high-fidelity rows finalized.")
    return df_analysis


def clean_and_prepare_data(df):
    df_clean = df.dropna(subset=['virial_energy_j', 'discriminant', 'logmass', 'distance_mpc', 'density_kg_m3']).copy()
    df_clean = df_clean[np.isfinite(df_clean['discriminant']) & (df_clean['discriminant'] != 0)]
    df_clean['scaling_constant_K'] = df_clean['virial_energy_j'] / df_clean['discriminant']
    
    df_clean.replace([np.inf, -np.inf], np.nan, inplace=True)
    df_clean.dropna(subset=['scaling_constant_K'], inplace=True)
    
    k_low, k_high = df_clean['scaling_constant_K'].quantile(0.01), df_clean['scaling_constant_K'].quantile(0.99)
    df_clean['K_clipped'] = df_clean['scaling_constant_K'].clip(k_low, k_high)
    return df_clean


def run_exploratory_analysis(df):
    print("  - Generating Bayesian Binning plot on full dataset...")
    # --- ROBUSTNESS FIX: Dynamic Binning ---
    try:
        # Bin redshift data
        z_bins_raw = pd.qcut(df['z'], q=5, duplicates='drop')
        num_z_bins = len(z_bins_raw.cat.categories)
        z_labels = [f"Q{i+1}" for i in range(num_z_bins)]
        df['redshift_bin'] = pd.qcut(df['z'], q=num_z_bins, labels=z_labels, duplicates='drop')
        
        # Bin density data
        density_bins_raw = pd.qcut(df['density_kg_m3'], q=5, duplicates='drop')
        num_density_bins = len(density_bins_raw.cat.categories)
        density_labels = [f"Q{i+1}" for i in range(num_density_bins)]
        df['density_bin'] = pd.qcut(df['density_kg_m3'], q=num_density_bins, labels=density_labels, duplicates='drop')
        
        binned_data = df.groupby(['redshift_bin', 'density_bin'], observed=False)['K_clipped'].mean().unstack()
        
        plt.figure(figsize=(12, 8)); sns.heatmap(binned_data, annot=True, fmt=".2e", cmap="viridis")
        plt.title("Bayesian Binning: Mean K by Redshift and Density Quantiles (Full Dataset)", fontsize=16)
        plt.xlabel("Mass Density Quantile", fontsize=12); plt.ylabel("Redshift Quantile", fontsize=12)
        plt.savefig(f"{OUTPUT_PLOT_PREFIX}_bayesian_binning.png"); plt.close()
    except Exception as e:
        print(f"    - Could not generate Bayesian Binning plot. Error: {e}")
        
    print("  - Generating KDE L-Function Analogue plot on full dataset...")
    plt.figure(figsize=(12, 7)); sns.kdeplot(data=df, x='K_clipped', fill=True)
    plt.title("KDE L-Function Analogue of Scaling Constant K (Full Dataset)", fontsize=16)
    plt.xlabel("Value of K (Clipped)", fontsize=12); plt.ylabel("Probability Density", fontsize=12)
    plt.savefig(f"{OUTPUT_PLOT_PREFIX}_kde_l_function.png"); plt.close()


def run_predictive_modeling(df):
    features = ['discriminant', 'z', 'logmass', 'petrorad_r', 'density_kg_m3']
    target = 'virial_energy_j'
    
    # Drop rows where any of the features or target are NaN before splitting
    df_model = df.dropna(subset=features + [target])
    
    X = df_model[features]
    y = df_model[target]
    
    if len(df_model) < 2:
        print("  - Not enough data to perform predictive modeling.")
        return
        
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=42)
    
    print(f"  - Data split into {len(X_train)} training samples and {len(X_test)} test samples.")
    
    pipeline = Pipeline([
        ('scaler', StandardScaler()),
        ('model', lgb.LGBMRegressor(random_state=42))
