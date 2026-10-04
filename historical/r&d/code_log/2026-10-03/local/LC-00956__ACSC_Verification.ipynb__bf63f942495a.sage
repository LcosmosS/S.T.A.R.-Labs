from sage.all import *            # initialize Sage internals
import csv, ast, sys, traceback, time
import pandas as pd
from sage.databases.cremona import CremonaDatabase
from tqdm import tqdm
import multiprocessing as mp
import os
from lmf import db as lmfdb_db


# ============== CONFIG ==============
IN = "lmfdb_raw_parsed.csv"          # Change to cremona for small test
OUT = "lmfdb_3selmer_estimates(1234).csv"
RESUME_FROM_LABEL = None             # e.g. "9990.p1" to resume
BATCH_FLUSH = 1000
# ====================================

# Try to import a PARI interface from multiple places
PARI_AVAILABLE = False
pari = None
try:
    # preferred: cypari2 if present
    from cypari2 import pari as _pari
    pari = _pari
    PARI_AVAILABLE = True
except Exception:
    try:
        # fallback: sage.interfaces.pari (may not exist in some builds)
        from sage.interfaces.pari import pari as _pari2
        pari = _pari2
        PARI_AVAILABLE = True
    except Exception:
        pari = None
        PARI_AVAILABLE = False

# Configuration
ATTEMPT_SAGE_RANK = True
ATTEMPT_PARI = PARI_AVAILABLE
ATTEMPT_3SEL_PROXY = True

def parse_a_invs(s):
    if not s:
        return None
    s = s.strip()
    try:
        if s.startswith("[") and s.endswith("]"):
            lst = ast.literal_eval(s)
        else:
            lst = [int(x) for x in s.replace(" ", "").split(",") if x!='']
        if len(lst) == 5:
            return [int(x) for x in lst]
    except Exception:
        return None
    return None

def compute_evidence_for_curve(label, a_raw):
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

    parsed = parse_a_invs(a_raw)
    if not parsed:
        evidence["notes"] = "no a-invariants"
        return evidence

    try:
        E = EllipticCurve(parsed)
    except Exception as e:
        evidence["notes"] = f"EllipticCurve construction failed: {e}"
        return evidence

    # 1) Sage rank (best-effort)
    if ATTEMPT_SAGE_RANK:
        try:
            r = E.rank()  # may raise "not provably correct"
            evidence["sage_rank"] = int(r)
        except Exception as e:
            evidence["sage_rank_error"] = str(e)
            evidence["sage_rank"] = None

    # 2) PARI evidence (if available)
    if ATTEMPT_PARI and pari is not None:
        try:
            pE = pari(E) if callable(pari) else None
            if pE is not None:
                # ellrank() return format can vary; attempt to extract 2-Selmer or rank
                try:
                    ellrank_res = pE.ellrank()
                    # prefer second entry if present (PARI often returns [rank, 2-Selmer, ...])
                    try:
                        if len(ellrank_res) >= 2:
                            evidence["pari_2_selmer_rank"] = int(ellrank_res[1])
                        else:
                            evidence["pari_2_selmer_rank"] = int(ellrank_res[0])
                    except Exception:
                        evidence["pari_2_selmer_rank"] = None
                except Exception as e:
                    evidence["notes"] += f" PARI ellrank failed: {e}"
                # analytic rank
                try:
                    an = pE.ellanalyticrank()
                    evidence["pari_analytic_rank"] = int(an[0])
                except Exception as e:
                    evidence["notes"] += f" PARI analytic failed: {e}"
        except Exception as e:
            evidence["notes"] += f" PARI interface call failed: {e}"

    # 3) torsion check (3-torsion proxy)
    try:
        tors = E.torsion_subgroup().order()
        evidence["has_rational_3_torsion"] = (int(tors) % 3 == 0)
    except Exception as e:
        evidence["has_rational_3_torsion"] = None
        evidence["notes"] += f" torsion check failed: {e}"

    # 4) 3-Selmer proxy heuristic
    if ATTEMPT_3SEL_PROXY:
        ranks = []
        if isinstance(evidence["sage_rank"], int):
            ranks.append(evidence["sage_rank"])
        if isinstance(evidence["pari_2_selmer_rank"], int):
            ranks.append(evidence["pari_2_selmer_rank"])
        if isinstance(evidence["pari_analytic_rank"], int):
            ranks.append(evidence["pari_analytic_rank"])

        numeric = [r for r in ranks if isinstance(r, int)]
        if numeric and min(numeric) == max(numeric):
            evidence["estimated_3_selmer_bound"] = numeric[0]
        else:
            evidence["estimated_3_selmer_bound"] = "Inconclusive"

    return evidence

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
                evidence = compute_evidence_for_curve(label, a_raw)
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

    print(f"\n✅ Finished! Wrote {OUT}")
    print(f"Total time: {int(time.time()-start_time)} seconds")

if __name__ == "__main__":
    main()