import pandas as pd
import numpy as np
from pathlib import Path
from sage.schemes.elliptic_curves.ec_database import elliptic_curves
from sage.all import QQ, EllipticCurve
import time
import random
from tqdm import tqdm
import concurrent.futures
import gc
import os


# ────── CONFIG (increased for your request) ──────
NUM_CURVES_PER_RANK = 150         # increased from 50
LMFDB_EXTRA_CURVES = 50           # new high-rank/unsolved curves from LMFDB
MAX_WORKERS = 4                   # safe on your Ryzen 5 5600X
GALAXIES_PER_CURVE = 60           # richer clusters
OUTPUT_DIR = Path("synthetic_cosmos_full")
OUTPUT_DIR.mkdir(exist_ok=True)
OUTPUT_CSV = OUTPUT_DIR / "synthetic_cosmic_catalog_full.csv"


print(f"🚀 FULL UPGRADE — Cremona full DB + LMFDB + {NUM_CURVES_PER_RANK} curves/rank")


def worker(label, rank, source="Cremona"):
    """Worker (runs in separate process)"""
    try:
        E = EllipticCurve(label)
        Reg = E.regulator() if rank > 0 else QQ(1)
        Omega = E.period_lattice().real_period()
        T = E.torsion_order()
        
        V_comove = float((Reg * Omega * T**2) ** (1/rank) * 1e6) if rank > 0 else 1e6
        rho_scale = float((Reg / (Omega * T**2)) ** (1/rank) * 1e3)
        
        return {
            'exact_rank': rank,
            'regulator': float(Reg),
            'real_period': float(Omega),
            'torsion': int(T),
            'V_comove': V_comove,
            'rho_scale': rho_scale,
            'betti_1': int(rank * 2 + random.randint(-1, 1)),
            'conductor': int(E.conductor()),
            'discriminant': float(E.discriminant()),
            'cremona_label': label,
            'source': source
        }
    except Exception as e:
        return {'error': str(e), 'label': label, 'rank': rank, 'source': source}


results = []


# === RANKS 1–3: Full Cremona Database (now complete) ===
for r in [1, 2, 3]:
    print(f"\n🔢 Rank {r} — Full Cremona DB ({NUM_CURVES_PER_RANK} curves)")
    labels = elliptic_curves.labels_with_rank(rank=r, conductor_max=500000)
    selected = random.sample(list(labels), min(NUM_CURVES_PER_RANK, len(labels)))
    
    with concurrent.futures.ProcessPoolExecutor(max_workers=MAX_WORKERS) as executor:
        future_to_label = {executor.submit(worker, label, r, "Cremona"): label for label in selected}
        for future in tqdm(concurrent.futures.as_completed(future_to_label), total=len(selected), desc=f"Rank {r} Cremona"):
            cosmo = future.result()
            if 'error' in cosmo:
                continue
            # Generate galaxies
            for g in range(GALAXIES_PER_CURVE):
                results.append({**cosmo,
                                'synthetic_RA': float(np.random.normal(0, cosmo['rho_scale']/10)),
                                'synthetic_DE': float(np.random.normal(0, cosmo['rho_scale']/10)),
                                'synthetic_z': float(np.random.normal(cosmo['V_comove']/3e5, 0.008)),
                                'galaxy_id': f"{cosmo['cremona_label']}_g{g}"})
    
    # Incremental save
    pd.DataFrame(results).to_csv(OUTPUT_CSV, mode='a', header=not os.path.exists(OUTPUT_CSV) or r==1, index=False)
    print(f"   ✓ Rank {r} saved — {len(results):,} galaxies so far")
    results = []
    gc.collect()


# === HIGH-RANK / UNSOLVED CURVES FROM LMFDB ===
print(f"\n🔢 Adding {LMFDB_EXTRA_CURVES} high-rank curves from LMFDB...")
# Known high-rank LMFDB labels (rank 4+); Sage can load them directly
lmfdb_high_rank_labels = [
    '5077a1', '1483a1', '1443c1', '1324a1', '1034a1',  # rank 3–4 examples
    # Add more known high-rank labels here if you want (we can expand later)
