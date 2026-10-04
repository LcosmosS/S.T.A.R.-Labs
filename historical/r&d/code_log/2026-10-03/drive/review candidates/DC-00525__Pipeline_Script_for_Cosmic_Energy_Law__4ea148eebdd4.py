# --- 1. Configuration ---
INPUT_FILE = 'merged_galspec_gz2.csv'
OUTPUT_PLOT_PREFIX = 'final_synthesis_v14'
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


from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score


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
    print("--- [STAGE 1/2] Starting HIGH-FIDELITY Data Processing... ---")
    df_analysis = process_data()
    if df_analysis is None or df_analysis.empty:
        print("Pipeline halted due to lack of valid data."); return
        
    print(f"\n--- [STAGE 2/2] Final Synthesis: Deriving K via Log-Log Regression... ---")
    df_clean = clean_and_prepare_data(df_analysis)
    if df_clean.empty:
        print("Pipeline halted: No valid data remained after log-transformation."); return
    
    run_final_synthesis(df_clean)


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
    df_clean = df.dropna(subset=['virial_energy_j', 'discriminant']).copy()
    
    # Take absolute values and filter out any zeros before log transform
    df_clean = df_clean[(df_clean['virial_energy_j'] != 0) & (df_clean['discriminant'] != 0)]
    
    df_clean['log_abs_virial_energy'] = np.log10(np.abs(df_clean['virial_energy_j']))
    df_clean['log_abs_discriminant'] = np.log10(np.abs(df_clean['discriminant']))
    
    # Drop any rows where log transform might have failed (e.g., from residual non-finite values)
    df_clean.replace([np.inf, -np.inf], np.nan, inplace=True)
    df_clean.dropna(subset=['log_abs_virial_energy', 'log_abs_discriminant'], inplace=True)
    
    print(f"  - Log-transformation complete. {len(df_clean)} numerically stable rows finalized for analysis.")
    return df_clean


def run_final_synthesis(df):
    X = df[['log_abs_discriminant']]
    y = df['log_abs_virial_energy']


    if X.empty or y.empty:
        print("  - Not enough data to perform linear regression."); return


    model = LinearRegression()
    model.fit(X, y)
    
    y_pred = model.predict(X)
    r2 = r2_score(y, y_pred)
    
    log_K = model.intercept_
    K = 10**log_K
    slope = model.coef_[0]
    
    print("\n" + "="*80)
    print("      DEFINITIVE SYNTHESIS: DERIVED SCALING CONSTANT & MODEL FIT")
    print("="*80)
    print(f"\nMETHODOLOGY:")
    print("A linear regression was performed on the log-transformed data, fitting the model:")
    print("  log(|Virial Energy|) = SLOPE * log(|Discriminant|) + log(|K|)\n")
    print("-" * 80)
    print("RESULTS:\n")
    print(f"  - Derived Slope (m): {slope:.6f}")
    print(f"     (Hypothesis predicts a slope of 1.0; a value close to 1 is a strong validation.)\n")
    print(f"  - Derived y-intercept (log10(|K|)): {log_K:.6f}")
    print(f"  - Data-Driven Scaling Constant (|K|): {K:.6e}\n")
    print(f"  - Model Fit (R² Score): {r2:.6f}")
    print(f"     (An R² score close to 1.0 indicates the model explains the vast majority")
    print(f"      of the variance in the data.)")
    print("="*80)


    print("\n  - Generating final Log-Log Regression plot...")
    plt.figure(figsize=(12, 8))
    sns.regplot(x=X['log_abs_discriminant'], y=y, scatter_kws={'alpha':0.1, 's':5}, line_kws={'color':'red', 'linewidth':2})
    plt.title("Final Synthesis: Log-Log Regression of Virial Energy vs. Discriminant", fontsize=16)
    plt.xlabel("log10(|Discriminant|)", fontsize=12)
    plt.ylabel("log10(|Virial Energy|)", fontsize=12)
    
    # Add annotation box with results
    results_text = (f"Derived Slope: {slope:.4f}\n"
                    f"Derived |K|: {K:.4e}\n"
                    f"R² Score: {r2:.4f}")
