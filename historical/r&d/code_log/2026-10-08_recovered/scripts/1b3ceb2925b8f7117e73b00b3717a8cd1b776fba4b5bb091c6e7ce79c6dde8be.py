import pandas as pd
from sage.databases.cremona import CremonaDatabase
from tqdm import tqdm
import multiprocessing as mp
import os

# ========================= CONFIG =========================
NUM_CORES = 4
CHUNK_SIZE = 400
OUTPUT_CREMONA = "cremona_raw_parsed.csv"
OUTPUT_LMFDB   = "lmfdb_raw_parsed.csv"
# ======================================================

print("=== CREMONA (already done) ===")
if os.path.exists(OUTPUT_CREMONA):
    n_cremona = sum(1 for _ in open(OUTPUT_CREMONA)) - 1
    print(f" {OUTPUT_CREMONA} already exists ({n_cremona:,} curves)")
else:
    print("Cremona file not found.")

# ====================== LMFDB (lmfdb-lite) ======================
print("\n=== LMFDB EXTRACTION (lmfdb-lite) ===")
from lmf import db as lmfdb_db

def lmfdb_batch(start, batch_size=10000):
    query = {"conductor": {"$gte": start, "$lt": start + batch_size}}
    results = list(lmfdb_db.ec_curvedata.search(
        query,
        ["lmfdb_label", "conductor", "absD", "rank", "ainvs"]   # ← exact column names from your list
    ))
    rows = []
    for r in results:
        rows.append({
            "label": r.get("lmfdb_label"),
            "conductor": int(r.get("conductor", 0)),
            "delta": int(r.get("absD", 0)),           # absolute discriminant = |Δ|
            "rank": int(r.get("rank", -1)),
            "a_invariants_raw": str(r.get("ainvs", [])),
        })
    return rows

all_lmfdb = []
BATCH_SIZE = 10000
max_cond = 500000   # increase to 1_000_000+ if you want more curves

for start in tqdm(range(1, max_cond, BATCH_SIZE), desc="LMFDB batches"):
    batch = lmfdb_batch(start, BATCH_SIZE)
    all_lmfdb.extend(batch)

df_lmfdb = pd.DataFrame(all_lmfdb)
df_lmfdb.to_csv(OUTPUT_LMFDB, index=False)

print(f"\n LMFDB raw parsed saved: {OUTPUT_LMFDB} ({len(df_lmfdb):,} curves)")

print("\n DONE! BOTH RAW CSVs ARE READY")
print(f"   cremona_raw_parsed.csv  → {n_cremona:,} curves (local Cremona)")
print(f"   lmfdb_raw_parsed.csv    → {len(df_lmfdb):,} curves (LMFDB)")
print("\nNext step:")
print("   python compute_3selmer_from_raw.py")
print("   (it will use cremona_raw_parsed.csv by default)")
print("   To use LMFDB instead, change the line:")
print("   IN = 'lmfdb_raw_parsed.csv'")
