import pandas as pd
import numpy as np
from concurrent.futures import ProcessPoolExecutor
import os
from pathlib import Path
import warnings

warnings.filterwarnings('ignore')

# ────── CONFIG ──────
CHUNK_SIZE = int(5000)          # force plain Python int
MAX_WORKERS = 3                 # safe for your 48 GB RAM / Ryzen 5
OUTPUT_DIR = Path("star_processed")
OUTPUT_DIR.mkdir(exist_ok=True)

print(f"DEBUG: CHUNK_SIZE = {CHUNK_SIZE} (type: {type(CHUNK_SIZE)})")
print(f"DEBUG: Output folder: {OUTPUT_DIR.absolute()}")

def safe_clip(df):
    numeric = df.select_dtypes(include=[np.number]).columns
    df[numeric] = np.clip(df[numeric], -1e12, 1e12)
    return df

# ────── 2MASS + Gaia DR3 processor ──────
def process_chunk_2mass_gaia(chunk, chunk_idx):
    chunk = chunk.copy()
    chunk = safe_clip(chunk)
    
    # Realistic distance modulus filter (only keep plausible galaxies)
    if 'DM' in chunk.columns:
        chunk = chunk[chunk['DM'] > 20]
    
    # Feature engineering using columns actually present in your file
    if 'DM' in chunk.columns and 'Vcmb' in chunk.columns:
        chunk['scaled_a'] = -chunk['DM'] * 50.0          # will be used later for elliptic curve
        chunk['scaled_b'] = chunk['Vcmb'] / 100.0
    else:
        chunk['scaled_a'] = np.nan
        chunk['scaled_b'] = np.nan
    
    # Gaia + 2MASS magnitude proxies
    if 'Gmag' in chunk.columns and 'Jmag' in chunk.columns:
        chunk['flux_gr'] = 10**(-0.4 * chunk['Gmag']) / (10**(-0.4 * chunk['Jmag']) + 1e-12)
    if 'Kmag' in chunk.columns:
        chunk['flux_rz_proxy'] = chunk.get('Jmag', 0) / (chunk['Kmag'] + 1e-8)
    
    # Simple position/velocity regime flag
    if 'Vcmb' in chunk.columns:
        chunk['predicted_regime'] = (chunk['Vcmb'] > 10000).astype(int)
    else:
        chunk['predicted_regime'] = 0
    
    out_file = OUTPUT_DIR / f"2mass_gaia_batch_{chunk_idx:05d}.parquet"
    chunk.to_parquet(out_file)
    print(f"✓ 2MASS-Gaia batch {chunk_idx} → {len(chunk):,} rows saved")
    return None

# ────── DESI DR8 + SDSS DR16 + SIMBAD processor ──────
def process_chunk_desi_sdss(chunk, chunk_idx):
    chunk = chunk.copy()
    chunk = safe_clip(chunk)
    
    if 'zphot' in chunk.columns:
        chunk['scaled_a'] = -chunk['zphot'] * 1000.0
        chunk['scaled_b'] = chunk.get('gmag', 0) * 10.0
    else:
        chunk['scaled_a'] = np.nan
        chunk['scaled_b'] = np.nan
    
    chunk['flux_gr'] = chunk.get('gmag', 0) / (chunk.get('rmag', 1) + 1e-8)
    
    if 'zphot' in chunk.columns:
        chunk['predicted_regime'] = (chunk['zphot'] > 0.1).astype(int)
    else:
        chunk['predicted_regime'] = 0
    
    out_file = OUTPUT_DIR / f"desi_sdss_batch_{chunk_idx:05d}.parquet"
    chunk.to_parquet(out_file)
    print(f"✓ DESI-SDSS batch {chunk_idx} → {len(chunk):,} rows saved")
    return None

def run_parallel_preprocessing(file_path, process_func, name):
    file_path = Path(file_path)
    if not file_path.exists():
        print(f"❌ ERROR: File not found → {file_path}")
        return
    
    print(f"\n🚀 Starting {name} preprocessing on {file_path.name} ...")
    
    reader = pd.read_csv(file_path, chunksize=CHUNK_SIZE, low_memory=False)
    
    with ProcessPoolExecutor(max_workers=MAX_WORKERS) as executor:
        futures = []
        for i, chunk in enumerate(reader):
            if chunk.empty:
                continue
            future = executor.submit(process_func, chunk, i)
            futures.append(future)
            
            # Keep memory low – wait every few batches
            if len(futures) >= MAX_WORKERS * 2:
                for f in futures:
                    f.result()
                futures = []
        
        # finish remaining
        for f in futures:
            f.result()
    
    print(f"✅ Finished preprocessing {file_path.name}\n")

# ────── RUN BOTH FILES ──────
run_parallel_preprocessing('JApJ94494_2MASS_GAIADR3_EPOCH.csv', 
                           process_chunk_2mass_gaia, "2MASS + Gaia")

run_parallel_preprocessing('DESIDR8_SDSSDR16_SIMBAD.csv', 
                           process_chunk_desi_sdss, "DESI + SDSS + SIMBAD")

print("🎉 Step 1 COMPLETE! All batches saved to folder: star_processed/")
print("Next: reply with 'step 2' and I will give you the exact-rank SageMath script.")