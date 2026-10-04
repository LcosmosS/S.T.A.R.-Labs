# acsc_validation_full_batch.py
import csv
import time
import gc
import traceback
import numpy as np
from tqdm import tqdm

# ============== CONFIG - CHANGE THESE FOR EACH RUN ==============
# Run this script TWICE: once for Cremona, once for LMFDB
PAIR = "lmfdb"          # Change to "lmfdb" for the second run

if PAIR == "lmfdb":
    THREE_SELMER_FILE = "lmfdb_3selmer_full_pari.csv"
    RAW_FILE = "lmfdb_raw_parsed.csv"
    OUTPUT_FILE = "acsc_validation_lmfdb.csv"
elif PAIR == "lmfdb":
    THREE_SELMER_FILE = "lmfdb_3selmer_full_pari.csv"
    RAW_FILE = "lmfdb_raw_parsed.csv"
    OUTPUT_FILE = "acsc_validation_lmfdb.csv"
else:
    raise ValueError("Set PAIR to 'cremona' or 'lmfdb'")

RESUME_FROM_LABEL = None          # set to a label to resume a crashed run
BATCH_FLUSH = 2000
# ========================================================

def parse_float(val):
    try:
        return float(val) if val not in ("", None, "None") else None
    except:
        return None

def passes_complexity_14(row, delta):
    """Exact Complexity-14 / SFT potential from our earlier conversation"""
    try:
        rank = parse_float(row.get("sage_rank"))
        conductor = parse_float(row.get("conductor", 1000))
        if rank is None or delta is None:
            return False

        log_abs_delta = np.log10(abs(delta) + 1)

        # Scarcity term (high-rank requires exponentially larger |Δ|)
        scarcity = log_abs_delta - (5.0 + 2.5 * rank)

        # Stability / normalization term (from SFT potential)
        stability = (rank / (np.log10(conductor) + 1)) ** 2

        # Pass only if both terms satisfy the Symbolic Action Principle
        return (scarcity > 0) and (stability < 10.0)
    except:
        return False

def main():
    start_time = time.time()
    print(f"Processing {THREE_SELMER_FILE} with {RAW_FILE}...")

    # Load delta lookup from raw file
    delta_dict = {}
    with open(RAW_FILE, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            label = row.get("label", "").strip()
            delta_dict[label] = parse_float(row.get("delta", 0))

    resume_found = RESUME_FROM_LABEL is None

    with open(THREE_SELMER_FILE, newline='', encoding='utf-8') as inf, \
         open(OUTPUT_FILE, 'w', newline='', encoding='utf-8') as outf:

        reader = csv.DictReader(inf)
        fieldnames = list(reader.fieldnames) + ["delta", "log_abs_delta", "passes_complexity_14"]
        writer = csv.DictWriter(outf, fieldnames=fieldnames)
        writer.writeheader()

        for i, row in enumerate(tqdm(reader, desc="ACSC Validation"), 1):
            label = row.get("label", "").strip()

            if not resume_found:
                if label == RESUME_FROM_LABEL:
                    resume_found = True
                continue

            delta = delta_dict.get(label, 0.0)
            log_abs_delta = np.log10(abs(delta) + 1) if delta != 0 else 0.0

            passes_14 = passes_complexity_14(row, delta)

            out_row = dict(row)
            out_row["delta"] = delta
            out_row["log_abs_delta"] = round(log_abs_delta, 6)
            out_row["passes_complexity_14"] = passes_14

            writer.writerow(out_row)

            if i % BATCH_FLUSH == 0:
                outf.flush()
                gc.collect()
                elapsed = int(time.time() - start_time)
                print(f"[{i:,}] processed {label}  elapsed={elapsed}s  (flushed)")

    print(f"\n Finished! Wrote {OUTPUT_FILE}")
    print(f"Total time: {int(time.time()-start_time)} seconds")

if __name__ == "__main__":
    main()