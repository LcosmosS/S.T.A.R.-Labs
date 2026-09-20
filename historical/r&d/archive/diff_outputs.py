#!/usr/bin/env python3
import os
import sys
import json
import numpy as np
import pandas as pd

from pathlib import Path

# ------------------------------
# CONFIGURATION
# ------------------------------
TOL_ABS = 1e-6
TOL_REL = 1e-4

FILES_TO_COMPARE = [
    "results/projection_points.csv",
    "results/entropy_summary.csv",
    "results/geodesics.npy",
    "results/delta_g_summary.csv",
    "results/hubble_fit_summary.json",
    "results/tda_landscape.npy",
]

# ------------------------------
# UTILITIES
# ------------------------------

def safe_load_csv(path):
    try:
        return pd.read_csv(path)
    except Exception:
        return None

def safe_load_json(path):
    try:
        with open(path) as f:
            return json.load(f)
    except Exception:
        return None

def safe_load_npy(path):
    try:
        return np.load(path, allow_pickle=True)
    except Exception:
        return None

def write(report_dir, name, text):
    with open(report_dir / name, "w") as f:
        f.write(text)

def numeric_diff(a, b):
    """Return max absolute and relative diff."""
    a = np.asarray(a)
    b = np.asarray(b)
    if a.shape != b.shape:
        return np.inf, np.inf
    abs_diff = np.max(np.abs(a - b))
    rel_diff = np.max(np.abs(a - b) / (np.abs(b) + 1e-12))
    return abs_diff, rel_diff

# ------------------------------
# MAIN DIFF LOGIC
# ------------------------------

def diff_csv(current, previous):
    if current is None or previous is None:
        return "Missing file in one of the runs", True

    if current.shape != previous.shape:
        return f"Shape mismatch: {current.shape} vs {previous.shape}", True

    diffs = []
    for col in current.columns:
        if col not in previous.columns:
            diffs.append(f"Column {col} missing in previous")
            continue
        a = current[col].values
        b = previous[col].values
        absd, reld = numeric_diff(a, b)
        diffs.append(f"{col}: abs={absd:.3e}, rel={reld:.3e}")

    # Determine if any diff exceeds tolerance
    fail = any(
        ("abs=" in d and float(d.split("abs=")[1].split(",")[0]) > TOL_ABS) or
        ("rel=" in d and float(d.split("rel=")[1]) > TOL_REL)
        for d in diffs
    )

    return "\n".join(diffs), fail

def diff_json(current, previous):
    if current is None or previous is None:
        return "Missing JSON file", True

    diffs = []
    fail = False

    keys = set(current.keys()) | set(previous.keys())
    for k in keys:
        if k not in current:
            diffs.append(f"{k}: missing in current")
            fail = True
            continue
        if k not in previous:
            diffs.append(f"{k}: missing in previous")
            fail = True
            continue

        a = current[k]
        b = previous[k]

        if isinstance(a, (int, float)) and isinstance(b, (int, float)):
            absd = abs(a - b)
            reld = abs(a - b) / (abs(b) + 1e-12)
            diffs.append(f"{k}: abs={absd:.3e}, rel={reld:.3e}")
            if absd > TOL_ABS or reld > TOL_REL:
                fail = True
        else:
            if a != b:
                diffs.append(f"{k}: {a} != {b}")
                fail = True

    return "\n".join(diffs), fail

def diff_npy(current, previous):
    if current is None or previous is None:
        return "Missing NPY file", True

    absd, reld = numeric_diff(current, previous)
    fail = absd > TOL_ABS or reld > TOL_REL
    return f"abs={absd:.3e}, rel={reld:.3e}", fail

# ------------------------------
# ENTRY POINT
# ------------------------------

def main():
    if len(sys.argv) != 4:
        print("Usage: diff_outputs.py <current_dir> <previous_dir> <report_dir>")
        sys.exit(1)

    current_dir = Path(sys.argv[1])
    previous_dir = Path(sys.argv[2])
    report_dir = Path(sys.argv[3])
    report_dir.mkdir(parents=True, exist_ok=True)

    overall_fail = False

    for relpath in FILES_TO_COMPARE:
        cur = current_dir / relpath
        prev = previous_dir / relpath

        report_name = relpath.replace("/", "_") + ".txt"

        if relpath.endswith(".csv"):
            result, fail = diff_csv(safe_load_csv(cur), safe_load_csv(prev))
        elif relpath.endswith(".json"):
            result, fail = diff_json(safe_load_json(cur), safe_load_json(prev))
        elif relpath.endswith(".npy"):
            result, fail = diff_npy(safe_load_npy(cur), safe_load_npy(prev))
        else:
            result = "Unsupported file type"
            fail = False

        write(report_dir, report_name, result)
        overall_fail = overall_fail or fail

    if overall_fail:
        print("Regression detected — see diff_report/")
        sys.exit(1)
    else:
        print("No significant regressions detected.")
        sys.exit(0)

if __name__ == "__main__":
    main()
