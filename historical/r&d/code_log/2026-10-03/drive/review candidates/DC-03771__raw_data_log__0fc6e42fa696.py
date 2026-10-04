import pandas as pd
from sage.all import EllipticCurve, QQ
import os
from pathlib import Path


BATCH_DIR = Path("star_processed")
OUTPUT_CSV = "star_exact_ranks.csv"


def compute_exact_rank_batch(batch_file):
    df = pd.read_parquet(batch_file)
    results = []
    for idx, row in df.iterrows():
        try:
            a = QQ(row['scaled_a'])
            b = QQ(row['scaled_b'])
            E = EllipticCurve(QQ, [0, 0, 0, a, b])
            rank = E.rank(algorithm='pari')          # exact, no heuristic
            disc = float(E.discriminant())
            conductor = E.conductor()
            results.append({
                'batch': batch_file.name,
                'row_idx': idx,
                'exact_rank': rank,
                'discriminant': disc,
                'conductor': conductor,
                'scaled_a': float(a),
                'scaled_b': float(b)
            })
        except Exception as e:
            results.append({'batch': batch_file.name, 'row_idx': idx, 'error': str(e)})
    pd.DataFrame(results).to_csv(OUTPUT_CSV, mode='a', header=not os.path.exists(OUTPUT_CSV), index=False)
    print(f"✓ Processed {batch_file.name} – {len(results)} curves")


# Process one batch at a time (very safe on 48 GB)
for f in sorted(BATCH_DIR.glob("*.parquet")):
    compute_exact_rank_batch(f)
