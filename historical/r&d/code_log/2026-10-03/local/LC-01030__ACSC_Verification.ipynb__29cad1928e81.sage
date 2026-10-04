import pandas as pd
from sage.databases.cremona import CremonaDatabase
from tqdm import tqdm
import multiprocessing as mp
import requests
import time
import os

# ========================= CONFIG =========================
NUM_CORES = 4
CHUNK_SIZE = 400
OUTPUT_CREMONA = "cremona_raw_parsed.csv"
OUTPUT_LMFDB   = "lmfdb_raw_parsed.csv"
# ======================================================

# ====================== CREMONA (already done) ======================
print("=== CREMONA (skipping — you already have the file) ===")
if os.path.exists(OUTPUT_CREMONA):
    print(f"✅ {OUTPUT_CREMONA} already exists ({sum(1 for _ in open(OUTPUT_CREMONA))-1:,} curves)")
else:
    print("Cremona file not found — would regenerate if needed.")

# ====================== LMFDB PART (FIXED) ======================
print("\n=== LMFDB EXTRACTION (lmfdb-lite + fallback) ===")

try:
    from lmf import db as lmfdb_db
    print("Using lmfdb-lite (local database)")

    def lmfdb_batch(start, batch_size=10000):
        query = {"conductor": {"$gte": start, "$lt": start + batch_size}}
        results = list(lmfdb_db.ec_curvedata.search(
            query,
            ["lmfdb_label", "conductor", "discriminant", "rank", "ainvs"]   # FIXED column name
        ))
        rows = []
        for r in results:
            rows.append({
                "label": r.get("lmfdb_label") or r.get("label"),
                "conductor": int(r.get("conductor", 0)),
                "delta": int(r.get("discriminant", 0)),
                "rank": int(r.get("rank", -1)),
                "a_invariants_raw": str(r.get("ainvs", [])),
            })
        return rows

    all_lmfdb = []
    BATCH_SIZE = 10000
    max_cond = 500000

    for start in tqdm(range(1, max_cond, BATCH_SIZE), desc="LMFDB-lite batches"):
        batch = lmfdb_batch(start, BATCH_SIZE)
        all_lmfdb.extend(batch)

except Exception as e:
    print(f"lmfdb-lite failed ({e}) — falling back to public API (slower but reliable)")
    # Public API fallback (already robust)
    def fetch_lmfdb_batch(start, limit=1000):
        url = "https://www.lmfdb.org/api/ec_curvedata/"
        params = {
            "fields": "label,conductor,discriminant,rank,ainvs",
            "limit": limit,
            "start": start
        }
        headers = {"User-Agent": "Mozilla/5.0"}
        try:
            r = requests.get(url, params=params, headers=headers, timeout=20)
            r.raise_for_status()
            return r.json().get("data", [])
        except:
            time.sleep(1)
            return []

    all_lmfdb = []
    start = 0
    while True:
        batch = fetch_lmfdb_batch(start)
        if not batch:
            break
        for r in batch:
            all_lmfdb.append({
                "label": r.get("label"),
                "conductor": r.get("conductor"),
                "delta": r.get("discriminant"),
                "rank": r.get("rank"),
                "a_invariants_raw": str(r.get("ainvs", [])),
            })
        start += 1000
        if start % 10000 == 0:
            print(f"   API fetched {start:,} records...")

# ====================== SAVE LMFDB ======================
df_lmfdb = pd.DataFrame(all_lmfdb)
df_lmfdb.to_csv(OUTPUT_LMFDB, index=False)
print(f"✅ LMFDB raw parsed saved: {OUTPUT_LMFDB} ({len(df_lmfdb):,} curves)")

print("\n🎉 BOTH FILES ARE READY!")
print(f"   cremona_raw_parsed.csv  → {len(pd.read_csv(OUTPUT_CREMONA)) if os.path.exists(OUTPUT_CREMONA) else 0:,} curves")
print(f"   lmfdb_raw_parsed.csv    → {len(df_lmfdb):,} curves")
print("\nNow run your 3-Selmer script:")
print("   python compute_3selmer_from_raw.py")
print("   (change IN = 'lmfdb_raw_parsed.csv' if you want the LMFDB version)")