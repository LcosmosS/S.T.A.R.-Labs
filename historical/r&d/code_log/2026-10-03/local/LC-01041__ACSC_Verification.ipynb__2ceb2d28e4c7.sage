# acsc_validation_full_batch.py
import csv
import time
import gc
import traceback
import numpy as np
from tqdm import tqdm

# ============== CONFIG ==============
FILES = [
    "cremona_3selmer_full_pari.csv",
    "lmfdb_3selmer_full_pari.csv"
]
BATCH_FLUSH = 2000
RESUME_FROM_LABEL = None          # set to a label if you need to resume
# ====================================

def parse_float(val):
    try:
        return float(val) if val not in ("", None, "None") else None
    except:
        return None

def passes_complexity_14(row):
    """Exact Complexity-14 + SFT potential logic from our earlier conversation"""
    try:
        rank = parse_float(row.get("sage_rank"))
        delta = parse_float(row.get("delta"))
        conductor = parse_float(row.get("conductor", 1000))

        if rank is None or delta is None:
            return False

        log_abs_delta = np.log10(abs(delta) + 1)

        # Complexity-14 / SFT potential (your constants)
        # λ term from PySR (0.4610, 0.4032) + Arithmetic Scarcity
        scarcity = log_abs_delta - (5.0 + 2.5 * rank)                    # rank-delta scarcity
        stability = (rank / (np.log10(conductor) + 1)) ** 2             # rank normalization

        # Pass only if both terms satisfy the symbolic action
        return (scarcity > 0) and (stability < 10.0)
    except:
        return False

def process_file(input_file):
    output_file = "acsc_validation_" + input_file.replace("_full_pari.csv", ".csv")
    print(f"\n=== Processing {input_file} → {output_file} ===")

    resume_found = RESUME_FROM_LABEL is None
    start_time = time.time()

    with open(input_file, newline='', encoding='utf-8') as inf, \
         open(output_file, 'w', newline='', encoding='utf-8') as outf:

        reader = csv.DictReader(inf)
        fieldnames = list(reader.fieldnames) + ["log_abs_delta", "passes_complexity_14"]
        writer = csv.DictWriter(outf, fieldnames=fieldnames)
        writer.writeheader()

        for i, row in enumerate(tqdm(reader, desc="ACSC batch"), 1):
            label = row.get("label", "").strip()

            if not resume_found:
                if label == RESUME_FROM_LABEL:
                    resume_found = True
                continue

            delta = parse_float(row.get("delta", 0))
            log_abs_delta = np.log10(abs(delta) + 1) if delta != 0 else 0.0

            passes_14 = passes_complexity_14(row)

            row["log_abs_delta"] = round(log_abs_delta, 6)
            row["passes_complexity_14"] = passes_14

            writer.writerow(row)

            if i % BATCH_FLUSH == 0:
                outf.flush()
                gc.collect()
                elapsed = int(time.time() - start_time)
                print(f"[{i}] processed {label}  elapsed={elapsed}s  (flushed)")

    print(f" Finished {input_file} → {output_file} ({i:,} rows)")

def main():
    for f in FILES:
        process_file(f)
    print("\n🎉 ALL ACSC VALIDATION FILES COMPLETE!")

if __name__ == "__main__":
    main()