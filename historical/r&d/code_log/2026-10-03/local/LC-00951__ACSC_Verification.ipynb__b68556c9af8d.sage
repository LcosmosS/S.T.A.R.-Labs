import pandas as pd
import numpy as np
from sage.databases.cremona import CremonaDatabase
from sage.schemes.elliptic_curves.ec_database import elliptic_curves
from sage.all import QQ, EllipticCurve
from tqdm import tqdm
import multiprocessing as mp
import os

# ========================= CONFIG =========================
OUTPUT_CSV = "acsc_cremona.csv"
NUM_CURVES_PER_RANK = 38042
NUM_CORES = 6
CHUNK_SIZE = 1000          # Smaller chunks = less memory pressure
RESTART_FROM = 1

# ======================================================

db = CremonaDatabase()
print(f"Using MiniCremonaDatabase — largest conductor = {db.largest_conductor():,}")

# ====================== WORKER FUNCTIONS ======================

def get_rank_worker(N):
    """Fast worker: only get rank and basic info (always reliable in mini-db)"""
    rows = []
    try:
        class_labels = db.curves(N)
        for cls in class_labels:
            label = f"{N}{cls}" if isinstance(cls, str) else f"{N}{cls[0]}"
            try:
                # Use low-level access for rank (very stable)
                rank = db.allcurves(N)[cls][1] if hasattr(db, 'allcurves') else db.elliptic_curve(label).rank()
                row = {
                    "label": label,
                    "conductor": N,
                    "delta": None,           # will fill later if possible
                    "rank": int(rank),
                    "regulator": None,
                    "real_period": None,
                    "tamagawa": None,
                    "sha": None,
                    "torsion": None,
                    "weierstrass_a_invariants": None,
                    "j_invariant": None,
                }
                rows.append(row)
            except:
                pass
    except:
        pass
    return rows
    
results = []

for r in [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16]:
    print(f"\n Rank {r} — fetching Cremona labels...")
    labels = elliptic_curves.rank(rank=r, n=NUM_CURVES_PER_RANK, labels=True)
    
    print(f"   Processing {len(labels)} curves in parallel...")

def get_bsd_worker(label):
    """Separate worker for heavy BSD invariants (omega, regulator, etc.)"""
    try:
        E = db.elliptic_curve(label)
        delta_val = int(E.discriminant())
        try:
            reg_val = float(E.regulator()) if E.rank() > 0 else 1.0
        except:
            reg_val = 1.0
            
        # Safe extraction
        try:
            omega_val = float(E.omega())
        except:
            omega_val = None
            
        try:
            reg_val = float(E.regulator()) if E.rank() > 0 else 1.0
        except:
            reg_val = 1.0
            
        try:
            tam_val = int(E.tamagawa_product())
        except:
            tam_val = None
            
        try:
            sha_val = float(E.sha())
        except:
            sha_val = None
            
        try:
            # Torsion is critical for your denominator weighting
            tors_val = int(E.torsion_order())
        except:
            tors_val = 1 # Default to 1 to avoid div by zero
            
        return {
            "label": label,
            "delta": int(E.discriminant()),
            "regulator": reg_val,
            "torsion": tors_val,
            "real_period": float(E.omega()) if hasattr(E, 'omega') else None,
            "conductor": int(E.conductor()),
            "rank": int(E.rank())
        }
    except:
        return None

# ====================== MAIN PARALLEL PIPELINE ======================

print(f"Starting parallel extraction with {NUM_CORES} cores...")

all_rows = []
conductors = list(range(RESTART_FROM, db.largest_conductor() + 1))

for i in tqdm(range(0, len(conductors), CHUNK_SIZE), desc="Rank phase (fast)"):
    chunk = conductors[i:i + CHUNK_SIZE]
    with mp.Pool(processes=NUM_CORES) as pool:
        chunk_results = pool.map(get_rank_worker, chunk)
    for res in chunk_results:
        all_rows.extend(res)

print(f"Rank phase complete: {len(all_rows):,} basic entries")

# Second pass: fill BSD invariants in parallel (only for labels we have)
labels_to_process = [row["label"] for row in all_rows if row["rank"] is not None]

print(f"Starting BSD invariants phase for {len(labels_to_process):,} curves...")

bsd_results = []
with mp.Pool(processes=NUM_CORES) as pool:
    for result in tqdm(pool.imap_unordered(get_bsd_worker, labels_to_process), total=len(labels_to_process), desc="BSD phase"):
        if result:
            bsd_results.append(result)

# Merge the two datasets
rank_df = pd.DataFrame(all_rows)
bsd_df = pd.DataFrame(bsd_results)

if not bsd_df.empty:
    final_df = pd.merge(rank_df, bsd_df, on="label", how="left", suffixes=("", "_bsd"))
   
    # Prefer BSD-filled values
    for col in ["delta", "regulator", "real_period", "tamagawa", "sha", "torsion", "weierstrass_a_invariants", "j_invariant"]:
        if col + "_bsd" in final_df.columns:
            final_df[col] = final_df[col + "_bsd"].combine_first(final_df[col])
            final_df.drop(columns=[col + "_bsd"], inplace=True)
else:
    final_df = rank_df

# ACSC derived columns
final_df["log_abs_delta"] = final_df["delta"].abs().apply(lambda x: float(x)**0.5 if pd.notna(x) and x != 0 else 0)
final_df["log_conductor"] = final_df["conductor"].apply(lambda x: float(x)**0.5 if pd.notna(x) and x != 0 else 0)
final_df['bsd_weight'] = final_df['regulator'] / (final_df['torsion']**2)

# Log-normalize the conductor to prevent the "blindness" effect in KDE
final_df['log_conductor'] = np.log10(final_df['conductor'] + 1)

# Create a robust scale for the Alpha Complex (0.1 to 5.0 range)
from sklearn.preprocessing import MinMaxScaler
scaler = MinMaxScaler(feature_range=(0.1, 5.0))
final_df['tda_weight'] = scaler.fit_transform(np.log1p(final_df[['bsd_weight']]))

final_df.to_csv(OUTPUT_CSV, index=False)

final_df.to_csv(OUTPUT_CSV, index=False)

print(f"\n Final ACSC dataset saved: {OUTPUT_CSV}")
print(f"   Total curves: {len(final_df):,}")
print(f"   real_period (omega) computed where available")
print("   Rank is fully populated (fast path)")

print("Ready for ACSC testing!")