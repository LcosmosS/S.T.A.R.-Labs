import pandas as pd
import numpy as np
from concurrent.futures import ProcessPoolExecutor
import os
from pathlib import Path
import warnings
warnings.filterwarnings('ignore')


CHUNK_SIZE = 5000
MAX_WORKERS = 3
OUTPUT_DIR = Path("star_processed")
OUTPUT_DIR.mkdir(exist_ok=True)


def safe_clip(df):
    numeric = df.select_dtypes(include=np.number).columns
    df[numeric] = np.clip(df[numeric], -1e12, 1e12)
    return df


def process_chunk_2mass_gaia(chunk, chunk_idx):
    chunk = chunk.copy()
    chunk = safe_clip(chunk)
    
    # Clean obvious bad values
    if 'DM' in chunk.columns:
        chunk = chunk[chunk['DM'] > 20]  # realistic distance modulus
    
    # Feature engineering using columns actually present in your file
    if 'DM' in chunk.columns and 'Vcmb' in chunk.columns:
        chunk['scaled_a'] = -chunk['DM'] * 50.0          # placeholder – you can tune this
        chunk['scaled_b'] = chunk['Vcmb'] / 100.0
    else:
        chunk['scaled_a'] = np.nan
        chunk['scaled_b'] = np.nan
    
    # Magnitude-based proxies (Gaia + 2MASS)
    if 'Gmag' in chunk.columns and 'Jmag' in chunk.columns:
        chunk['flux_gr'] = 10**(-0.4 * chunk['Gmag']) / (10**(-0.4 * chunk['Jmag']) + 1e-12)
    if 'Kmag' in chunk.columns:
        chunk['flux_rz_proxy'] = chunk.get('Jmag', 0) / (chunk['Kmag'] + 1e-8)
    
    # Position features
    if all(col in chunk.columns for col in ['RAJ2000', 'DEJ2000']):
        chunk['pm_mag_proxy'] = np.sqrt(chunk.get('pmRA', 0)**2 + chunk.get('pmDE', 0)**2)
    
    # Regime (galactic vs cluster) – using velocity or redshift proxy
    if 'Vcmb' in chunk.columns:
        chunk['predicted_regime'] = (chunk['Vcmb'] > 10000).astype(int)
    else:
        chunk['predicted_regime'] = 0
    
    chunk.to_parquet(OUTPUT_DIR / f"2mass_gaia_batch_{chunk_idx:05d}.parquet")
    print(f"✓ 2MASS-Gaia batch {chunk_idx} done")
    return None  # we already wrote to disk


def process_chunk_desi_sdss(chunk, chunk_idx):
    chunk = chunk.copy()
    chunk = safe_clip(chunk)
    
    # Similar features using DESI/SDSS columns
    if 'zphot' in chunk.columns:
        chunk['scaled_a'] = -chunk['zphot'] * 1000.0
        chunk['scaled_b'] = chunk.get('gmag', 0) * 10.0
    chunk['flux_gr'] = chunk.get('gmag', 0) / (chunk.get('rmag', 1) + 1e-8)
    
    if 'RAdeg' in chunk.columns and 'DEdeg' in chunk.columns:
        chunk['pm_mag_proxy'] = 0.0  # placeholder
    
    if 'zphot' in chunk.columns:
        chunk['predicted_regime'] = (chunk['zphot'] > 0.1).astype(int)
    else:
        chunk['predicted_regime'] = 0
    
    chunk.to_parquet(OUTPUT_DIR / f"desi_sdss_batch_{chunk_idx:05d}.parquet")
    print(f"✓ DESI-SDSS batch {chunk_idx} done")
    return None


def run_parallel_preprocessing(file_path, process_func, prefix):
    reader = pd.read_csv(file_path, chunksize=CHUNK_SIZE, low_memory=False)
    with ProcessPoolExecutor(max_workers=MAX_WORKERS) as executor:
        futures = []
        for i, chunk in enumerate(reader):
            if chunk.empty:
                continue
            future = executor.submit(process_func, chunk, i)
            futures.append(future)
            if len(futures) >= MAX_WORKERS * 2:
                for f in futures:
                    f.result()  # wait and let it write
                futures = []
        # remaining
        for f in futures:
            f.result()
    print(f"✅ Finished preprocessing {file_path}")


# === RUN ON YOUR TWO FILES ===
run_parallel_preprocessing('JApJ94494_2MASS_GAIADR3_EPOCH.csv', process_chunk_2mass_gaia, "2mass_gaia")
run_parallel_preprocessing('DESIDR8_SDSSDR16_SIMBAD.csv', process_chunk_desi_sdss, "desi_sdss")


print("Preprocessing complete. All batches saved to star_processed/ folder.")
