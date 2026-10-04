# compute_sage_invariants.py
from sage.all import *
from sage.databases.cremona import CremonaDatabase
import csv, sys

db = CremonaDatabase()
labels = [l.strip() for l in open("labels.txt") if l.strip()]
out = "cremona_sage_invariants.csv"
with open(out, "w", newline='') as f:
    w = csv.writer(f)
    w.writerow(["label","conductor","rank","regulator","sha","tamagawa_product","torsion_order","real_period","a_invariants","j_invariant"])
    for lab in labels:
        try:
            E = db.elliptic_curve(lab)
            a_invs = E.a_invariants()
            j = E.j_invariant()
            cond = E.conductor()
            rank = E.rank()
            reg = E.regulator() if hasattr(E, "regulator") else ""
            sha = E.sha() if hasattr(E, "sha") else ""
            tam = 1
            for p in E.tamagawa_numbers().values():
                tam *= p
            tors = E.torsion_subgroup().order()
            realp = E.real_period()
            w.writerow([lab, cond, rank, reg, sha, tam, tors, realp, list(a_invs), j])
        except Exception as e:
            w.writerow([lab, "ERROR", str(e)])
print("Wrote", out)

