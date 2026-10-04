# compute_3selmer_from_raw.py
# Robust 3-Selmer evidence pipeline using Sage + optional PARI backend.
from sage.all import *            # initialize Sage internals
import csv, ast, sys, traceback, time

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

IN = "cremona_raw_parsed.csv"
OUT = "cremona_3selmer_estimates.csv"

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

def main():
    start = time.time()
    with open(IN, newline='', encoding='utf-8') as inf, open(OUT, 'w', newline='', encoding='utf-8') as outf:
        r = csv.DictReader(inf)
        fieldnames = [
            "label","used_a_invariants","sage_rank","sage_rank_error",
            "pari_2_selmer_rank","pari_analytic_rank","has_rational_3_torsion",
            "estimated_3_selmer_bound","notes"
        ]
        w = csv.DictWriter(outf, fieldnames=fieldnames)
        w.writeheader()
        for i,row in enumerate(r, start=1):
            label = row.get("label","")
            a_raw = row.get("a_invariants_raw","") or row.get("a_invariants","")
            try:
                evidence = compute_evidence_for_curve(label, a_raw)
                w.writerow(evidence)
            except Exception as e:
                w.writerow({
                    "label": label,
                    "used_a_invariants": a_raw,
                    "sage_rank": "",
                    "sage_rank_error": str(e),
                    "pari_2_selmer_rank": "",
                    "pari_analytic_rank": "",
                    "has_rational_3_torsion": "",
                    "estimated_3_selmer_bound": "ERROR",
                    "notes": "exception during processing"
                })
                traceback.print_exc()
            if i % 50 == 0:
                print(f"[{i}] processed {label} elapsed={int(time.time()-start)}s")
    print("Wrote", OUT)

if __name__ == "__main__":
    main()
