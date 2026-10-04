#!/usr/bin/env sage -python
# -*- coding: utf-8 -*-

import sys, os, csv, argparse, time
from joblib import Parallel, delayed
from sageall import EllipticCurve, pari

# ----------------------------------------------------------------------
# PARI defaults for each worker
# ----------------------------------------------------------------------
def init_pari():
    pari.default('two_seconds', 10**9)     # effectively no timeout
    pari.default('primelimit', 10**7)
    pari.default('seriesprecision', 50)

# ----------------------------------------------------------------------
# Compute invariants for a single label
# ----------------------------------------------------------------------
def compute_one(label):
    init_pari()
    row = {
        "label": label,
        "conductor": None,
        "discriminant": None,
        "j_invariant": None,
        "omega_real": None,
        "torsion_order": None,
        "tamagawa_product": None,
        "rank_algebraic": None,
        "rank_analytic_pari": None,
        "selmer2_rank_pari": None,
        "sha_order": None,
        "heegner_height": None,
        "error": None,
    }

    try:
        E = EllipticCurve(label)
    except Exception as e:
        row["error"] = f"EllipticCurve init failed: {e}"
        return row

    try: row["conductor"] = int(E.conductor())
    except: pass

    try: row["discriminant"] = int(E.discriminant())
    except: pass

    try: row["j_invariant"] = E.j_invariant()
    except: pass

    try: row["omega_real"] = float(E.real_period())
    except: pass

    try: row["torsion_order"] = int(E.torsion_subgroup().order())
    except: pass

    try:
        tams = E.tamagawa_numbers()
        prod = 1
        for t in tams: prod *= int(t)
        row["tamagawa_product"] = prod
    except: pass

    try: row["rank_algebraic"] = int(E.rank())
    except: pass

    # Analytic rank via PARI
    try:
        gE = pari(E)
        rdata = gE.ellrankinit()
        row["rank_analytic_pari"] = int(gE.ellrank(rdata))
    except Exception as e:
        row["rank_analytic_pari"] = None
        row["error"] = f"analytic rank error: {e}"

    # 2-Selmer rank
    try:
        row["selmer2_rank_pari"] = int(E.selmer_rank(2))
    except Exception as e:
        row["selmer2_rank_pari"] = None

    # Sha (optional)
    try:
        sha = E.sha()
        if sha is not None:
            row["sha_order"] = int(sha.order())
    except:
        pass

    # Heegner height (simple proxy)
    try:
        gens = E.gens()
        if gens:
            row["heegner_height"] = float(E.height(gens[0]))
    except:
        pass

    return row

# ----------------------------------------------------------------------
# Main
# ----------------------------------------------------------------------
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--labels-file", required=True)
    parser.add_argument("--output", required=True)
    parser.add_argument("--workers", type=int, default=4)
    parser.add_argument("--batch-size", type=int, default=500)
    args = parser.parse_args()

    # Load labels
    labels = []
    with open(args.labels_file) as f:
        reader = csv.DictReader(f)
        for r in reader:
            labels.append(r["label"].strip())

    print(f"Loaded {len(labels)} labels")

    # Prepare output
    out_path = args.output
    os.makedirs(os.path.dirname(out_path), exist_ok=True)

    fieldnames = [
        "label",
        "conductor",
        "discriminant",
        "j_invariant",
        "omega_real",
        "torsion_order",
        "tamagawa_product",
        "rank_algebraic",
        "rank_analytic_pari",
        "selmer2_rank_pari",
        "sha_order",
        "heegner_height",
        "error",
    ]

    write_header = not os.path.exists(out_path)

    t0 = time.time()
    processed = 0

    with open(out_path, "a", newline="") as fout:
        writer = csv.DictWriter(fout, fieldnames=fieldnames)
        if write_header:
            writer.writeheader()

        # Parallel processing in batches
        for i in range(0, len(labels), args.batch_size):
            batch = labels[i:i+args.batch_size]
            results = Parallel(n_jobs=args.workers, backend="loky")(
                delayed(compute_one)(lab) for lab in batch
            )
            writer.writerows(results)
            fout.flush()
            processed += len(batch)
            dt = time.time() - t0
            print(f"[{processed}/{len(labels)}] processed in {dt:.1f}s")

    print(f"Done. Total time: {time.time()-t0:.1f}s")
    print(f"Output written to {out_path}")

if __name__ == "__main__":
    main()
