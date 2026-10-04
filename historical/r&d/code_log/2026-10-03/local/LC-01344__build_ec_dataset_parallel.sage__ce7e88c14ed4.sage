import sys
import os
import csv
import json
import argparse
import time
import traceback
from joblib import Parallel, delayed
from sage.all import EllipticCurve, pari, QQ

# ----------------------------------------------------------------------
# Paths
# ----------------------------------------------------------------------
REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
ECDATA_ROOT = os.path.join(REPO_ROOT, "data", "ecdata")
LMFDB_ROOT = os.path.join(REPO_ROOT, "data", "lmfdb")

print(f"ECDATA_ROOT: {ECDATA_ROOT}")
print(f"LMFDB_ROOT: {LMFDB_ROOT}")

# ----------------------------------------------------------------------
# Worker initialization
# ----------------------------------------------------------------------
def init_worker():
    """Initialize PARI defaults for each worker."""
    try:
        pari.default('two_seconds', 10**9)
        pari.default('realprecision', 50)
    except:
        pass

# ----------------------------------------------------------------------
# Load from local submodules
# ----------------------------------------------------------------------
def load_cremona(label):
    """Load from Cremona ecdata format."""
    import re
    m = re.match(r"(\d+)([a-z]+)(\d+)", label)
    if not m:
        return None
    N, iso, num = m.groups()
    path = os.path.join(ECDATA_ROOT, N, iso, label)
    if not os.path.exists(path):
        return None
    data = {}
    try:
        with open(path) as f:
            for line in f:
                line = line.strip()
                if line.startswith("a-invariants:"):
                    parts = line.split(":")[1].strip().split()
                    data["ainvs"] = [int(x) for x in parts]
                elif line.startswith("conductor:"):
                    data["conductor"] = int(line.split(":")[1])
                elif line.startswith("torsion:"):
                    data["torsion"] = int(line.split(":")[1])
                elif line.startswith("tamagawa:"):
                    data["tamagawa"] = int(line.split(":")[1])
    except:
        return None
    return data if "ainvs" in data else None


def load_lmfdb(label):
    """Load from LMFDB JSON format."""
    import re
    m = re.match(r"(\d+)([a-z]+)(\d+)", label)
    if not m:
        return None
    N, iso, num = m.groups()
    json_path = os.path.join(LMFDB_ROOT, "elliptic_curves", N, iso, f"{label}.json")
    if not os.path.exists(json_path):
        return None
    try:
        with open(json_path) as f:
            j = json.load(f)
        return {
            "ainvs": j.get("ainvs"),
            "conductor": j.get("conductor"),
            "torsion": j.get("torsion_order"),
            "tamagawa": j.get("tamagawa_product"),
            "rank_lmfdb": j.get("rank"),
        }
    except:
        return None


def load_curve_data(label):
    """Unified loader with fallback."""
    d = load_cremona(label)
    if d is not None:
        return d
    return load_lmfdb(label)


# ----------------------------------------------------------------------
# Core computation (safe, single curve)
# ----------------------------------------------------------------------
def compute_one(label):
    init_worker()
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
        "selmer2_rank": None,
        "sha_order": None,
        "heegner_height": None,
        "error": None,
    }

    try:
        data = load_curve_data(label)
        if data is None or "ainvs" not in data:
            row["error"] = "Curve not found in ecdata or lmfdb"
            return row

        # Build curve
        E = EllipticCurve(data["ainvs"])

        # Basic invariants
        row["conductor"] = int(E.conductor())
        row["discriminant"] = int(E.discriminant())
        row["j_invariant"] = int(E.j_invariant())
        row["omega_real"] = float(E.period_lattice().real_period())
        row["torsion_order"] = int(E.torsion_order())
        row["tamagawa_product"] = int(E.tamagawa_product())

        # Rank (robust)
        try:
            E.two_descent(second_limit=20)
            row["rank_algebraic"] = int(E.rank(only_use_mwrank=False))
        except:
            try:
                row["rank_algebraic"] = int(E.rank_bound())
            except:
                row["rank_algebraic"] = None

        # Analytic rank via PARI
        try:
            gE = pari(E)
            rdata = gE.ellrankinit()
            row["rank_analytic_pari"] = int(gE.ellrank(rdata))
        except Exception as e:
            row["error"] = f"analytic rank: {str(e)[:100]}"

        # Selmer rank
        try:
            row["selmer2_rank"] = int(E.selmer_rank(2))
        except:
            pass

        # Sha
        try:
            sha = E.sha()
            if sha is not None:
                row["sha_order"] = int(sha.order())
        except:
            pass

        # Heegner / generator height
        try:
            gens = E.gens()
            if gens:
                row["heegner_height"] = float(E.height(gens[0]))
        except:
            pass

    except Exception as e:
        row["error"] = f"General error: {str(e)[:150]}"
        print(f"Error processing {label}: {e}", file=sys.stderr)

    return row


# ----------------------------------------------------------------------
# Main
# ----------------------------------------------------------------------
def main():
    parser = argparse.ArgumentParser(description="Safe EC dataset builder")
    parser.add_argument("--labels-file", required=True, help="CSV with labels")
    parser.add_argument("--output", required=True, help="Output CSV")
    parser.add_argument("--workers", type=int, default=2, help="Number of workers (CI: keep low)")
    parser.add_argument("--batch-size", type=int, default=100)
    args = parser.parse_args()

    # Load labels
    labels = []
    with open(args.labels_file) as f:
        reader = csv.DictReader(f)
        for r in reader:
            lab = r["label"].strip()
            if lab:
                labels.append(lab)

    print(f"Loaded {len(labels)} labels")
    print(f"Using {args.workers} workers, batch size {args.batch_size}")

    # Prepare output
    out_path = args.output
    os.makedirs(os.path.dirname(out_path), exist_ok=True)

    fieldnames = [
        "label", "conductor", "discriminant", "j_invariant", "omega_real",
        "torsion_order", "tamagawa_product", "rank_algebraic",
        "rank_analytic_pari", "selmer2_rank", "sha_order",
        "heegner_height", "error"
    ]

    write_header = not os.path.exists(out_path)
    t0 = time.time()
    processed = 0

    with open(out_path, "a", newline="") as fout:
        writer = csv.DictWriter(fout, fieldnames=fieldnames)
        if write_header:
            writer.writeheader()

        # Batch processing
        for i in range(0, len(labels), args.batch_size):
            batch = labels[i:i + args.batch_size]

            # Use 'threading' to avoid pickling issues
            if args.workers > 1:
                results = Parallel(n_jobs=args.workers, backend="threading")(
                    delayed(compute_one)(lab) for lab in batch
                )
            else:
                results = [compute_one(lab) for lab in batch]

            writer.writerows(results)
            fout.flush()

            processed += len(batch)
            dt = time.time() - t0
            print(f"[{processed}/{len(labels)}] processed in {dt:.1f}s")

    print(f"\n✅ Done. Total time: {time.time()-t0:.1f}s")
    print(f"Output written to: {out_path}")


if __name__ == "__main__":
    main()
