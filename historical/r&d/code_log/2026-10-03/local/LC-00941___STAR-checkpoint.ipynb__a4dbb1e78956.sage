import pandas as pd
from sage.all import EllipticCurve, QQ
from pathlib import Path
import os
import time
from tqdm import tqdm   # tqdm is usually available in SageMath

# ────── CONFIG ──────
BATCH_DIR = Path("star_processed")
OUTPUT_CSV = "star_exact_ranks.csv"
MAX_COEFF = 1000000         # safety limit – skip huge curves

print(f"DEBUG: Processing batches from {BATCH_DIR.absolute()}")
print(f"DEBUG: Will skip any curve where |a| or |b| > {MAX_COEFF:,}")

batch_files = sorted(BATCH_DIR.glob("*.parquet"))
print(f"Found {len(batch_files)} batches")

if os.path.exists(OUTPUT_CSV):
    done_batches = pd.read_csv(OUTPUT_CSV)['batch'].unique().tolist()
    print(f"Resuming — {len(done_batches)} batches already done")
else:
    done_batches = []

for batch_idx, batch_file in enumerate(batch_files):
    if str(batch_file.name) in done_batches:
        print(f"⏭️  Skipping already processed: {batch_file.name}")
        continue

    print(f"\n🚀 Starting batch {batch_idx+1}/{len(batch_files)} → {batch_file.name}")
    start_batch = time.time()
    
    df = pd.read_parquet(batch_file)
    results = []
    
    # tqdm progress bar for rows
    for idx, row in tqdm(df.iterrows(), total=len(df), desc=f"Batch {batch_idx+1}", leave=False):
        try:
            a_val = float(row.get('scaled_a', float('nan')))
            b_val = float(row.get('scaled_b', float('nan')))
            
            # Safety checks
            if pd.isna(a_val) or pd.isna(b_val):
                continue
            if abs(a_val) > MAX_COEFF or abs(b_val) > MAX_COEFF:
                results.append({'batch': batch_file.name, 'row_idx': idx,
                                'scaled_a': a_val, 'scaled_b': b_val,
                                'exact_rank': 'skipped_too_large'})
                continue
            
            # Show exactly which curve we are computing
            if idx % 20 == 0:   # print every 20 rows so you can see progress
                print(f"   → Row {idx} | a={a_val:.4f} | b={b_val:.4f}")
            
            row_start = time.perf_counter()
            
            E = EllipticCurve(QQ, [0, 0, 0, a_val, b_val])
            rank = E.rank(algorithm='pari', pari_effort=100)   # faster but still exact
            
            elapsed = time.perf_counter() - row_start
            
            results.append({
                'batch': batch_file.name,
                'row_idx': idx,
                'scaled_a': a_val,
                'scaled_b': b_val,
                'exact_rank': rank,
                'discriminant': float(E.discriminant()),
                'conductor': int(E.conductor()),
                'time_sec': round(elapsed, 3)
            })
            
        except Exception as e:
            results.append({
                'batch': batch_file.name,
                'row_idx': idx,
                'scaled_a': a_val if 'a_val' in locals() else None,
                'scaled_b': b_val if 'b_val' in locals() else None,
                'error': str(e)
            })
        
        # Save after EVERY row so nothing is lost
        if results:
            pd.DataFrame(results).to_csv(OUTPUT_CSV, mode='a',
                                         header=not os.path.exists(OUTPUT_CSV) or len(done_batches)==0,
                                         index=False)
            results = []   # clear buffer
    
    elapsed_batch = time.time() - start_batch
    print(f"   ✓ Batch {batch_idx+1} finished in {elapsed_batch:.1f} seconds")

print("\n🎉 STEP 2 COMPLETE!")
print(f"Exact ranks (with progress & safety) saved to → {OUTPUT_CSV}")
print("You can now open the CSV and see columns: exact_rank, time_sec, etc.")

print("\nReply with exactly: **step 3** when you are ready for the final ML + Entropy Cohomology script.")