#!/usr/bin/env sage -python
# -*- coding: utf-8 -*-

"""
Build a cross-referenced elliptic curve dataset (~40k rows) with:
- label
- conductor
- discriminant (Delta)
- j-invariant
- omega (real period)
- torsion order
- product of Tamagawa numbers
- algebraic rank (Sage)
- analytic rank (PARI)
- 2-Selmer rank (PARI-backed)
- optional: Sha order (if available)
- optional: simple Heegner height (if computable)

Usage (example):

    sage -python scripts/build_ec_dataset.sage \
        --labels-file data/raw/curve_labels.csv \
        --output data/processed/ec_invariants_full.csv \
        --batch-size 500

The labels file must have a column named 'label' with Cremona/LMFDB labels.
"""

import sys, os, csv, argparse, math, time
from sageall import (
    EllipticCurve,
    pari,
    ZZ,
)

# ----------------------------------------------------------------------
# PARI configuration: high two_seconds, no practical timeout
# ----------------------------------------------------------------------
pari.default('two_seconds', 10**9)   # effectively "no timeout"
# You can also tweak other defaults if needed:
# pari.default('primelimit', 10**7)

# ----------------------------------------------------------------------
# Argument parsing
# ----------------------------------------------------------------------
def parse_args():
    p = argparse.ArgumentParser(description="Build elliptic curve invariant dataset.")
    p.add_argument(
        "--labels-file",
        type=str,
        required=True,
        help="CSV file with at least a 'label' column (Cremona/LMFDB labels).",
    )
    p.add_argument(
        "--output",
        type=str,
        required=True,
        help="Output CSV path.",
    )
    p.add_argument(
        "--batch-size",
        type=int,
        default=500,
        help="Number of curves per write batch.",
    )
    return p.parse_args()

# ----------------------------------------------------------------------
# Helpers
# ----------------------------------------------------------------------
def safe_float(x):
    try:
        return float(x)
    except Exception:
        return None

def compute_invariants_for_label(label):
    """
    Given a Cremona/LMFDB label, construct E and compute:
    - conductor
    - discriminant
    - j-invariant
    - omega (real period)
    - torsion order
    - Tamagawa product
    - algebraic rank (Sage)
    - analytic rank (PARI)
    - 2-Selmer rank (PARI-backed)
    - Sha order (if available)
    - simple Heegner height (if computable; placeholder)
    """
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
    }

    try:
        E = EllipticCurve(label)
    except Exception as e:
        row["error"] = f"EllipticCurve init failed: {e}"
        return row

    # Basic invariants
    try:
        row["conductor"] = int(E.conductor())
    except Exception:
        pass

    try:
        row["discriminant"] = int(E.discriminant())
    except Exception:
        pass

    try:
        row["j_invariant"] = E.j_invariant()
    except Exception:
        pass

    try:
        row["omega_real"] = safe_float(E.real_period())
    except Exception:
        pass

    try:
        row["torsion_order"] = int(E.torsion_subgroup().order())
    except Exception:
        pass

    try:
        tams = E.tamagawa_numbers()
        prod_tam = 1
        for t in tams:
            prod_tam *= int(t)
        row["tamagawa_product"] = prod_tam
    except Exception:
        pass

    # Algebraic rank (Sage)
    try:
        row["rank_algebraic"] = int(E.rank())
    except Exception:
        pass

    # Analytic rank via PARI
    try:
        # Convert to PARI elliptic curve
        gE = pari(E)
        # ellrankinit returns structure; ellrank extracts analytic rank
        # This uses PARI's analytic machinery with our high two_seconds.
        rdata = gE.ellrankinit()
        r_analytic = gE.ellrank(rdata)
        row["rank_analytic_pari"] = int(r_analytic)
    except Exception as e:
        row["rank_analytic_pari_error"] = str(e)

    # 2-Selmer rank via Sage (PARI-backed)
    try:
        # This is typically PARI-backed under the hood.
        s2 = E.selmer_rank(2)
        row["selmer2_rank_pari"] = int(s2)
    except Exception as e:
        row["selmer2_rank_pari_error"] = str(e)

    # Sha order (if available; can be expensive)
    try:
        sha = E.sha()
        if sha is not None:
            row["sha_order"] = int(sha.order())
    except Exception:
        # Many curves will not have Sha computed; that's fine.
        pass

    # Heegner height (very rough placeholder; you can refine)
    try:
        # This is a placeholder: you can choose discriminants and compute
        # actual Heegner points; here we just record canonical height of a generator if any.
        gens = E.gens()
        if gens:
            P = gens[0]
            row["heegner_height"] = safe_float(E.height(P))
    except Exception:
        pass

    return row

# ----------------------------------------------------------------------
# Main
# ----------------------------------------------------------------------
def main():
    args = parse_args()

    labels = []
    with open(args.labels_file, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        if "label" not in reader.fieldnames:
            raise ValueError("labels-file must have a 'label' column.")
        for r in reader:
            lab = r["label"].strip()
            if lab:
                labels.append(lab)

    print(f"Loaded {len(labels)} labels from {args.labels_file}")

    # Prepare output
    out_path = args.output
    out_dir = os.path.dirname(out_path)
    if out_dir and not os.path.exists(out_dir):
        os.makedirs(out_dir, exist_ok=True)

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
        "rank_analytic_pari_error",
        "selmer2_rank_pari_error",
    ]

    # If file exists, we append; else we create and write header
    write_header = not os.path.exists(out_path)

    processed = 0
    t0 = time.time()

    with open(out_path, "a", newline="", encoding="utf-8") as f_out:
        writer = csv.DictWriter(f_out, fieldnames=fieldnames)
        if write_header:
            writer.writeheader()

        batch = []
        for i, lab in enumerate(labels, start=1):
            row = compute_invariants_for_label(lab)
            batch.append(row)

            if len(batch) >= args.batch_size:
                writer.writerows(batch)
                f_out.flush()
                processed += len(batch)
                batch = []
                dt = time.time() - t0
                print(f"[{processed}/{len(labels)}] curves processed in {dt:.1f}s")

        # Flush remaining
        if batch:
            writer.writerows(batch)
            f_out.flush()
            processed += len(batch)

    dt = time.time() - t0
    print(f"Done. Processed {processed} curves in {dt:.1f}s")
    print(f"Output written to: {out_path}")

if __name__ == "__main__":
    main()
