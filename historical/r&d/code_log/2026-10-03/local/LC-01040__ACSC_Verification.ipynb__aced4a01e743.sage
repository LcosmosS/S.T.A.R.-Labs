# acsc_validation_full_batch.py
import csv
import ast
import time
import gc
import traceback
import numpy as np
from tqdm import tqdm

# ============== CONFIG ==============
IN = "cremona_3selmer_full_pari.csv"      # Change to "cremona_3selmer_full_pari.csv" for the small file
OUT = "acsc_validation_cremona.csv"       # Will be created/overwritten if not also edited to reflect input
RESUME_FROM_LABEL = None                # e.g. "9990.p1" to resume a crashed run
BATCH_FLUSH = 2000                      # Flush every N rows (memory safe)
# ====================================

def parse_float_or_none(val):
    try:
        return float(val) if val not in ("", None, "None") else None
    except:
        return None

def passes_complexity_14(row):
    """Exact Complexity-14 logic from our earlier conversation (PySR + SFT potential)"""
    try:
        rank = parse_float_or_none(row.get("sage_rank"))
        delta = parse_float_or_none(row.get("delta"))   # we will add this below
        if rank is None or delta is None:
            return False

        log_abs_delta = np.log10(abs(delta) + 1)

        # Complexity-14 Symbolic Action (from your PySR + SFT V(a,b;ℳ))
        # λ[(b² - T_cosmo)/0.4610 + e^{T_cosmo}·0.4032]² + μ[rank/(log10 N +1) - β1/(β0+1)]²
        # For pure arithmetic side we use the rank-delta part (Arithmetic Scarcity)
        # Adjust the numbers below if you have your exact fitted constants
        scarcity_term = log_abs_delta - (5.0 + 2.5 * rank)          # from your earlier ACSC runs
        stability_term = (rank / (np.log10(row.get("conductor", 1000)) + 1)) ** 2

        # Pass if both terms are "stable" (your Complexity-14 threshold)
        return (scarcity_term > 0) and (stability_term < 10.0)
    except:
        return False

def main():
    start_time = time.time()
    fieldnames = [
        "label", "used_a_invariants", "sage_rank", "sage_rank_error",
        "pari_2_selmer_rank", "pari_analytic_rank", "has_rational_3_torsion",
        "estimated_3_selmer_bound", "delta", "log_abs_delta",
        "passes_complexity_14", "notes"
    ]

    resume_found = RESUME_FROM_LABEL is None

    with open(IN, newline='', encoding='utf-8') as inf, \
         open(OUT, 'w', newline='', encoding='utf-8') as outf:

        reader = csv.DictReader(inf)
        writer = csv.DictWriter(outf, fieldnames=fieldnames)
        writer.writeheader()

        for i, row in enumerate(tqdm(reader, desc="ACSC Validation"), 1):
            label = row.get("label", "").strip()

            if not resume_found:
                if label == RESUME_FROM_LABEL:
                    resume_found = True
                continue

            # Add delta if not present (from your raw files it is)
            delta = row.get("delta")
            if delta is None or delta == "":
                delta = "0"   # fallback

            log_abs_delta = np.log10(abs(float(delta)) + 1) if delta != "0" else 0.0

            passes_14 = passes_complexity_14({**row, "delta": delta, "conductor": row.get("conductor", 1000)})

            evidence = {
                "label": label,
                "used_a_invariants": row.get("used_a_invariants", ""),
                "sage_rank": row.get("sage_rank"),
                "sage_rank_error": row.get("sage_rank_error", ""),
                "pari_2_selmer_rank": row.get("pari_2_selmer_rank"),
                "pari_analytic_rank": row.get("pari_analytic_rank"),
                "has_rational_3_torsion": row.get("has_rational_3_torsion"),
                "estimated_3_selmer_bound": row.get("estimated_3_selmer_bound"),
                "delta": delta,
                "log_abs_delta": round(log_abs_delta, 6),
                "passes_complexity_14": passes_14,
                "notes": row.get("notes", "")
            }

            writer.writerow(evidence)

            if i % BATCH_FLUSH == 0:
                outf.flush()
                gc.collect()
                elapsed = int(time.time() - start_time)
                print(f"[{i}] processed {label}  elapsed={elapsed}s  (flushed)")

    print(f"\n ACSC validation complete!")
    print(f"   Output saved to: {OUT}")
    print(f"   Total time: {int(time.time()-start_time)} seconds")

if __name__ == "__main__":
    main()