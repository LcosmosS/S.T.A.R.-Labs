import pandas as pd
from sage.all import EllipticCurve, QQ
from pathlib import Path
import os
import time


# ────── CONFIG ──────
BATCH_DIR = Path("star_processed")
OUTPUT_CSV = "star_exact_ranks.csv"
MAX_BATCHES_TO_PROCESS = None   # set to e.g. 10 for a quick test run


print(f"DEBUG: Looking for batches in {BATCH_DIR.absolute()}")
print(f"DEBUG: Output file will be {OUTPUT_CSV}")


# Get all parquet files, sorted so we always process in the same order
batch_files = sorted(BATCH_DIR.glob("*.parquet"))
print(f"Found {len(batch_files)} batches to process")


if not batch_files:
    print("❌ No parquet files found! Did Step 1 complete successfully?")
    raise FileNotFoundError("No batches in star_processed/")


# Load existing results to make it resumable
if os.path.exists(OUTPUT_CSV):
    done_batches = pd.read_csv(OUTPUT_CSV)['batch'].unique().tolist()
    print(f"Resuming — already processed {len(done_batches)} batches")
else:
    done_batches = []


# Main processing loop (one batch at a time)
for i, batch_file in enumerate(batch_files):
    if MAX_BATCHES_TO_PROCESS is not None and i >= MAX_BATCHES_TO_PROCESS:
        print("Reached test limit — stopping early")
        break
    
    if str(batch_file.name) in done_batches:
        print(f"⏭️  Skipping already done: {batch_file.name}")
        continue
    
    print(f"\n🚀 Processing batch {i+1}/{len(batch_files)} → {batch_file.name}")
    start_time = time.time()
    
    try:
        df = pd.read_parquet(batch_file)
        print(f"   Loaded {len(df):,} rows")
        
        results = []
        for idx, row in df.iterrows():
            try:
                a_val = float(row.get('scaled_a', float('nan')))
                b_val = float(row.get('scaled_b', float('nan')))
                
                if pd.isna(a_val) or pd.isna(b_val):
                    continue  # skip rows with missing scaling
                
                # Create the elliptic curve
                E = EllipticCurve(QQ, [0, 0, 0, a_val, b_val])
                
                # Exact rank using PARI (no heuristic)
                rank = E.rank(algorithm='pari')
                disc = float(E.discriminant())
                conductor = int(E.conductor())
                
                results.append({
                    'batch': batch_file.name,
                    'row_idx': idx,
                    'scaled_a': a_val,
                    'scaled_b': b_val,
                    'exact_rank': rank,
                    'discriminant': disc,
                    'conductor': conductor
                })
                
            except Exception as e:
                results.append({
                    'batch': batch_file.name,
                    'row_idx': idx,
                    'error': str(e)
                })
        
        # Append to CSV (header only on first write)
        pd.DataFrame(results).to_csv(
            OUTPUT_CSV,
            mode='a',
            header=not os.path.exists(OUTPUT_CSV) or len(done_batches) == 0,
            index=False
        )
        
        elapsed = time.time() - start_time
        print(f"   ✓ Done — {len(results):,} curves processed in {elapsed:.1f} seconds")
        
    except Exception as e:
        print(f"   ❌ Critical error on {batch_file.name}: {e}")
        continue


print("\n🎉 STEP 2 COMPLETE!")
print(f"Exact ranks saved to → {OUTPUT_CSV}")
print("You can now open star_exact_ranks.csv and see the ranks column.")
print("\nReply with exactly: **step 3**  when you are ready for the final stacked ML + Entropy Cohomology script.")
