# compute_3selmer_with_full_pari.py - lmfdb
import csv
import ast
import time
import gc
import traceback
from tqdm import tqdm

# ============== CONFIG ==============
IN = "lmfdb_raw_parsed.csv"          # or "cremona_raw_parsed.csv"
OUT = "lmfdb_3selmer_full_pari.csv"
RESUME_FROM_LABEL = None             # set to resume, e.g. "9990.p1"
BATCH_FLUSH = 1000
# ====================================

# Increase PARI stack significantly (helps a lot)
try:
    from cypari2 import pari
    pari.allocatemem(2**31)   # 2 GiB — adjust if your machine has more RAM
    print("PARI stack set to ~2 GiB")
except Exception as e:
    print("Could not set PARI stack:", e)

def parse_a_invs(s):
    if not s or s in ("[]", ""):
        return None
    try:
        if s.startswith("[") and s.endswith("]"):
            return ast.literal_eval(s)
        else:
            return [int(x.strip()) for x in s.replace(" ", "").split(",") if x.strip()]
    except:
        return None

def compute_full_evidence(label, a_raw):
    evidence = {
        "label": label,
        "used_a_invariants": a_raw,
        "sage_rank": None,
        "sage_rank_error": "",
        "pari_2_selmer_rank": None,
        "pari_analytic_rank": None,
        "has_rational_3_torsion": None,
        "estimated_3_selmer_bound": "Inconclusive",
        "notes": ""
    }

    a_invs = parse_a_invs(a_raw)
    if not a_invs:
        evidence["notes"] = "invalid a-invariants"
        return evidence

    # Build curve once
    try:
        E = EllipticCurve(a_invs)
    except Exception as e:
        evidence["notes"] = f"curve construction failed: {e}"
        return evidence

    # 1. Sage algebraic rank (with isolation)
    try:
        evidence["sage_rank"] = int(E.rank())
    except Exception as e:
        evidence["sage_rank_error"] = str(e)[:150]

    # 2. PARI 2-Selmer and analytic rank (the part you want)
    try:
        pE = pari(E)
        # ellrank() typically returns [rank, 2-Selmer rank, ...]
        ellrank_res = pE.ellrank()
        if len(ellrank_res) >= 2:
            evidence["pari_2_selmer_rank"] = int(ellrank_res[1])
        else:
            evidence["pari_2_selmer_rank"] = int(ellrank_res[0])

        # Analytic rank
        an = pE.ellanalyticrank()
        evidence["pari_analytic_rank"] = int(an[0])
    except Exception as e:
        evidence["notes"] += f" PARI failed: {str(e)[:100]}"

    # 3. Torsion (safe)
    try:
        tors = E.torsion_subgroup().order()
        evidence["has_rational_3_torsion"] = (int(tors) % 3 == 0)
    except:
        pass

    # 4. 3-Selmer proxy using all available ranks
    ranks = []
    if isinstance(evidence["sage_rank"], int):
        ranks.append(evidence["sage_rank"])
    if isinstance(evidence["pari_2_selmer_rank"], int):
        ranks.append(evidence["pari_2_selmer_rank"])
    if isinstance(evidence["pari_analytic_rank"], int):
        ranks.append(evidence["pari_analytic_rank"])

    if ranks:
        if min(ranks) == max(ranks):
            evidence["estimated_3_selmer_bound"] = min(ranks)
        else:
            evidence["estimated_3_selmer_bound"] = f"Bounded {min(ranks)}–{max(ranks)}"

    # Cleanup
    del E, pE
    gc.collect()

    return evidence

def main():
    start_time = time.time()
    fieldnames = ["label","used_a_invariants","sage_rank","sage_rank_error",
                  "pari_2_selmer_rank","pari_analytic_rank","has_rational_3_torsion",
                  "estimated_3_selmer_bound","notes"]

    resume_found = RESUME_FROM_LABEL is None

    with open(IN, newline='', encoding='utf-8') as inf, \
         open(OUT, 'w', newline='', encoding='utf-8') as outf:

        reader = csv.DictReader(inf)
        writer = csv.DictWriter(outf, fieldnames=fieldnames)
        writer.writeheader()

        for i, row in enumerate(tqdm(reader, desc="Processing curves"), 1):
            label = row.get("label", "").strip()
            a_raw = row.get("a_invariants_raw", "") or row.get("a_invariants", "")

            if not resume_found:
                if label == RESUME_FROM_LABEL:
                    resume_found = True
                continue

            try:
                evidence = compute_full_evidence(label, a_raw)
                writer.writerow(evidence)
            except Exception as e:
                writer.writerow({
                    "label": label,
                    "used_a_invariants": a_raw,
                    "sage_rank": "",
                    "sage_rank_error": str(e)[:200],
                    "pari_2_selmer_rank": "",
                    "pari_analytic_rank": "",
                    "has_rational_3_torsion": "",
                    "estimated_3_selmer_bound": "ERROR",
                    "notes": "exception"
                })

            if i % BATCH_FLUSH == 0:
                outf.flush()
                gc.collect()
                elapsed = int(time.time() - start_time)
                print(f"[{i}] processed {label}  elapsed={elapsed}s  (flushed)")

    print(f"\n Finished writing {OUT} with full PARI data where possible")
    print(f"Total time: {int(time.time()-start_time)} seconds")

if __name__ == "__main__":
    main()
