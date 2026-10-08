import sys, os, csv, json, argparse, time
from sageall import EllipticCurve, pari, ZZ

# ----------------------------------------------------------------------
# PARI configuration
# ----------------------------------------------------------------------
pari.default('two_seconds', 10**9)

# ----------------------------------------------------------------------
# Paths to submodules
# ----------------------------------------------------------------------
REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
ECDATA_ROOT = os.path.join(REPO_ROOT, "data", "ecdata")
ECLIB_ROOT  = os.path.join(REPO_ROOT, "data", "eclib")
LMFDB_ROOT  = os.path.join(REPO_ROOT, "data", "lmfdb")

# ----------------------------------------------------------------------
# Load Cremona ecdata
# ----------------------------------------------------------------------
def load_cremona_from_ecdata(label):
    """
    Load a curve from data/ecdata/<conductor>/<isogeny>/<label>
    Returns dict with keys:
        a_invariants, conductor, torsion, ...
    or None if not found.
    """
    try:
        N, iso, num = label.split()
    except:
        # Cremona labels are like "11a1"
        # Parse manually
        import re
        m = re.match(r"(\d+)([a-z]+)(\d+)", label)
        if not m:
            return None
        N, iso, num = m.groups()

    path = os.path.join(ECDATA_ROOT, N, iso, f"{N}{iso}{num}")
    if not os.path.exists(path):
        return None

    data = {}
    with open(path) as f:
        for line in f:
            if line.startswith("a-invariants"):
                parts = line.split(":")[1].strip().split()
                data["a_invariants"] = list(map(int, parts))
            elif line.startswith("conductor"):
                data["conductor"] = int(line.split(":")[1])
            elif line.startswith("torsion"):
                data["torsion"] = int(line.split(":")[1])
            elif line.startswith("tamagawa"):
                data["tamagawa"] = int(line.split(":")[1])

    return data if "a_invariants" in data else None

# ----------------------------------------------------------------------
# Load LMFDB JSON
# ----------------------------------------------------------------------
def load_lmfdb(label):
    """
    Load curve from data/lmfdb/elliptic_curves/<N>/<iso>/<label>.json
    """
    try:
        import re
        m = re.match(r"(\d+)([a-z]+)(\d+)", label)
        if not m:
            return None
        N, iso, num = m.groups()
    except:
        return None

    json_path = os.path.join(
        LMFDB_ROOT, "elliptic_curves", N, iso, f"{label}.json"
    )
    if not os.path.exists(json_path):
        return None

    with open(json_path) as f:
        j = json.load(f)

    return {
        "a_invariants": j["ainvs"],
        "conductor": j["conductor"],
        "torsion": j["torsion_order"],
        "tamagawa": j.get("tamagawa_product"),
        "rank_lmfdb": j.get("rank"),
    }

# ----------------------------------------------------------------------
# Compute invariants
# ----------------------------------------------------------------------
def compute_invariants(label):
    row = {"label": label}

    # Try Cremona ecdata
    data = load_cremona_from_ecdata(label)

    # If not found, try LMFDB
    if data is None:
        data = load_lmfdb(label)

    if data is None:
        row["error"] = "Curve not found in ecdata or lmfdb"
        return row

    # Build curve
    try:
        E = EllipticCurve(data["a_invariants"])
    except Exception as e:
        row["error"] = f"Failed to construct curve: {e}"
        return row

    # Basic invariants
    try:
        row["conductor"] = int(E.conductor())
        row["discriminant"] = int(E.discriminant())
        row["j_invariant"] = int(E.j_invariant())
        row["torsion_order"] = int(E.torsion_order())
        row["omega_real"] = float(E.period_lattice().real_period())
        row["tamagawa_product"] = int(E.tamagawa_product())
    except Exception as e:
        row["error"] = f"Invariant error: {e}"

    # Algebraic rank
    try:
        row["rank_algebraic"] = int(E.rank())
    except Exception as e:
        row["error"] = f"rank error: {e}"

    # Analytic rank via PARI
    try:
        gE = pari(E)
        rdata = gE.ellrankinit()
        row["rank_analytic_pari"] = int(gE.ellrank(rdata))
    except Exception as e:
        row["rank_analytic_pari_error"] = str(e)

    # 2-Selmer rank
    try:
        row["selmer2_rank_pari"] = int(E.selmer_rank(2))
    except Exception as e:
        row["selmer2_rank_pari_error"] = str(e)

    # Sha
    try:
        sha = E.sha()
        if sha is not None:
            row["sha_order"] = int(sha.order())
    except:
        pass

    # Heegner height (placeholder)
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
    p = argparse.ArgumentParser()
    p.add_argument("--labels-file", required=True)
    p.add_argument("--output", required=True)
    p.add_argument("--batch-size", type=int, default=500)
    args = p.parse_args()

    labels = []
    with open(args.labels_file) as f:
        reader = csv.DictReader(f)
        for r in reader:
            labels.append(r["label"])

    out_dir = os.path.dirname(args.output)
    if out_dir and not os.path.exists(out_dir):
        os.makedirs(out_dir)

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

    write_header = not os.path.exists(args.output)

    with open(args.output, "a") as f_out:
        writer = csv.DictWriter(f_out, fieldnames=fieldnames)
        if write_header:
            writer.writeheader()

        batch = []
        t0 = time.time()

        for i, lab in enumerate(labels, 1):
            row = compute_invariants(lab)
            batch.append(row)

            if len(batch) >= args.batch_size:
                writer.writerows(batch)
                batch = []
                print(f"[{i}/{len(labels)}] processed")

        if batch:
            writer.writerows(batch)

    print("Done.")

if __name__ == "__main__":
    main()
