# dump_cremona_csv.py
from sage.all import *          # ensure Sage core is initialized
from sage.databases.cremona import CremonaDatabase
import csv

db = CremonaDatabase()
max_conductor = db.largest_conductor()

with open("cremona_ellcurves_invariants.csv", "w", newline="") as f:
    w = csv.writer(f)
    w.writerow([
        "label", "conductor", "rank", "discriminant", "regulator",
        "torsion_order", "real_period", "tamagawa_product",
        "sha_order", "a_invariants", "j_invariant", "omega"
    ])

    # iterate over conductors (stop early if you want)
    for N in db.conductors():
        # optional: skip very large N to test quickly
        # if N > 20000: break
        for label in db.curves(N):
            try:
                E = db.elliptic_curve(label)
            except Exception:
                continue

            def safe(fn, *args):
                try:
                    return fn(*args)
                except Exception:
                    return None

            row = [
                label,
                int(N),
                safe(E.rank),
                safe(E.discriminant),
                safe(E.regulator),
                safe(lambda: E.torsion_subgroup().order()),
                safe(E.real_period),
                safe(E.tamagawa_product),
                safe(lambda: (E.sha() and E.sha().order())),
                safe(lambda: list(E.ainvs())),
                safe(E.j_invariant),
                safe(lambda: E.omega())
            ]
            w.writerow(row)

print("Wrote cremona_ellcurves_invariants.csv")
