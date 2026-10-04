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

# ────── CONFIG (tune these safely) ──────
NUM_CURVES_PER_RANK = 50          # start low; increase to 100+ later
MAX_CONDUCTOR = 200000
MAX_WORKERS = 4                   # safe on your 6-core Ryzen (leave 2 cores free)
GALAXIES_PER_CURVE = 40           # reduced to prevent memory spikes
OUTPUT_DIR = Path("synthetic_cosmos_parallel")
OUTPUT_DIR.mkdir(exist_ok=True)
OUTPUT_CSV = OUTPUT_DIR / "synthetic_cosmic_catalog.csv"

print(f"🚀 PARALLEL synthetic cosmos (ACSC forward) — using {MAX_WORKERS} cores")
print(f"   Ryzen 5 5600X multi-core mode enabled\n")

def worker(label, rank):
    """Worker function (runs in separate process)"""
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
            'cremona_label': label
        }
    except Exception as e:
        return {'error': str(e), 'label': label, 'rank': rank}

results = []

for r in [1, 2, 3]:
    print(f"\n🔢 Rank {r} — fetching Cremona labels...")
    labels = elliptic_curves.rank(rank=r, n=NUM_CURVES_PER_RANK, labels=True)
    selected_labels = random.sample(list(labels), min(NUM_CURVES_PER_RANK, len(labels)))
    
    print(f"   Processing {len(selected_labels)} curves in parallel...")
    
    with concurrent.futures.ProcessPoolExecutor(max_workers=MAX_WORKERS) as executor:
        future_to_label = {executor.submit(worker, label, r): label for label in selected_labels}
        
        for future in tqdm(concurrent.futures.as_completed(future_to_label), total=len(selected_labels), desc=f"Rank {r}"):
            cosmo = future.result()
            if 'error' in cosmo:
                print(f"   ⚠️ Skipped {cosmo['label']}: {cosmo['error']}")
                continue
            
            # Generate synthetic galaxies (fast part)
            n_galaxies = GALAXIES_PER_CURVE
            ra = np.random.normal(0, cosmo['rho_scale']/10, n_galaxies)
            dec = np.random.normal(0, cosmo['rho_scale']/10, n_galaxies)
            z = np.random.normal(cosmo['V_comove']/3e5, 0.008, n_galaxies)
            
            for g in range(n_galaxies):
                results.append({
                    **cosmo,
                    'synthetic_RA': float(ra[g]),
                    'synthetic_DE': float(dec[g]),
                    'synthetic_z': float(z[g]),
                    'galaxy_id': f"{cosmo['cremona_label']}_g{g}"
                })
    
    # Incremental save + memory cleanup
    df_rank = pd.DataFrame(results)
    df_rank.to_csv(OUTPUT_CSV, mode='a', header=not os.path.exists(OUTPUT_CSV) or r==1, index=False)
    print(f"   ✓ Rank {r} saved — {len(results):,} synthetic galaxies so far")
    results = []  # clear for next rank
    gc.collect()

print(f"\n🎉 PARALLEL SYNTHETIC COSMOS COMPLETE!")
print(f"   → Total galaxies generated: {len(pd.read_csv(OUTPUT_CSV)):,}")
print(f"   → File: {OUTPUT_CSV}")
print(f"   → Ranks: 1, 2, 3 (pure arithmetic seeds)")

print("\nSummary:")
print(pd.read_csv(OUTPUT_CSV).groupby('exact_rank')[['V_comove', 'rho_scale', 'betti_1']].mean().round(2))

print("\nReply with one of:")
print("   • 'compare synthetic'   → compare this to your real JApJ/DESIDR8 data")
print("   • 'increase curves'      → run with more curves per rank")
print("   • 'add LMFDB'           → include unsolved/high-rank curves")
print("   • 'step 3'               → full ML + Entropy Cohomology on synthetic data")