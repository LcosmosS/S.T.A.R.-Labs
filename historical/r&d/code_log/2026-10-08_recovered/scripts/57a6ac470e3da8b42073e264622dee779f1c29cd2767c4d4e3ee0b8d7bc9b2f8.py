"""
ec_curvedata.py
A lightweight loader for Cremona curvedata using the git submodule
located at data/ecdata/curvedata/.

This replaces:  from lmf import db
"""

import os
import re

# ----------------------------------------------------------------------
# Locate repo root and ecdata directory
# ----------------------------------------------------------------------
REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
CURVEDATA_DIR = os.path.join(REPO_ROOT, "data", "ecdata", "curvedata")

if not os.path.isdir(CURVEDATA_DIR):
    raise RuntimeError(f"curvedata directory not found: {CURVEDATA_DIR}")


# ----------------------------------------------------------------------
# Parse a single curvedata line
# Format example:
#   11a1  [0,1,1,-10,-20]  11  -20  1728  ...
# ----------------------------------------------------------------------
def parse_curvedata_line(line):
    parts = line.strip().split()
    if len(parts) < 3:
        return None

    label = parts[0]

    # Extract a-invariants: "[0,1,1,-10,-20]"
    ainv_match = re.search(r"\[(.*?)\]", line)
    if not ainv_match:
        return None
    ainvs = list(map(int, ainv_match.group(1).split(",")))

    # Extract conductor (next integer after ainvs)
    rest = line[line.index("]") + 1 :].strip().split()
    try:
        conductor = int(rest[0])
    except:
        conductor = None

    return {
        "label": label,
        "ainvs": ainvs,
        "conductor": conductor,
        "raw": line.strip(),
    }


# ----------------------------------------------------------------------
# Load all curvedata.* chunk files
# ----------------------------------------------------------------------
def load_all_curvedata():
    rows = []
    for fname in sorted(os.listdir(CURVEDATA_DIR)):
        if not fname.startswith("curvedata."):
            continue
        path = os.path.join(CURVEDATA_DIR, fname)
        with open(path) as f:
            for line in f:
                if line.strip():
                    row = parse_curvedata_line(line)
                    if row:
                        rows.append(row)
    return rows


# ----------------------------------------------------------------------
# Build in-memory database
# ----------------------------------------------------------------------
print("Loading curvedata from submodule:", CURVEDATA_DIR)
rows = load_all_curvedata()

# Build lookup by label
by_label = {r["label"]: r for r in rows}

# Expose available columns
search_cols = ["label", "ainvs", "conductor", "raw"]


# ----------------------------------------------------------------------
# Public API (mimics lmf.db.ec_curvedata)
# ----------------------------------------------------------------------
class CurveDataDB:
    def __init__(self, rows, by_label):
        self.rows = rows
        self.by_label = by_label
        self.search_cols = search_cols

    def get(self, label):
        return self.by_label.get(label)

    def search(self, **kwargs):
        """
        Example:
            db.search(conductor=11)
        """
        results = self.rows
        for key, val in kwargs.items():
            results = [r for r in results if r.get(key) == val]
        return results


db = CurveDataDB(rows, by_label)

# ----------------------------------------------------------------------
# Demo
# ----------------------------------------------------------------------
if __name__ == "__main__":
    print("Available columns in ec_curvedata:")
    print(db.search_cols)
    print(f"Loaded {len(rows)} curves.")
