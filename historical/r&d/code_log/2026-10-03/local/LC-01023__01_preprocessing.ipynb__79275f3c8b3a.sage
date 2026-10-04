#!/usr/bin/env python3
"""
arithmetic_pipeline_light.py

- Safe streaming of large CSVs
- Robust parsing of used_a_invariants
- Exact rational discriminant and j-invariant computation (no Sage required)
- Merge with optional selmer/parsed tables by 'label'
- Output: arithmetic_verified.csv and arithmetic_pipeline_log.txt
"""

import os
import sys
import csv
import ast
import math
from fractions import Fraction
from typing import Optional, Tuple, List, Any

import pandas as pd

# === CONFIG ===
DATA_DIR = "."  # change to folder with your CSVs
PRIMARY = "cremona_from_raw_invariants.csv"
PARSed = "cremona_raw_parsed.csv"
SEL3_LMFDB = "lmfdb_3selmer_full_pari.csv"
SEL3_CREM = "cremona_3selmer_full_pari.csv"
OTHER_FILES = ["DESIDR8_SDSSDR16_SIMBAD.csv", "JApJ94494_2MASS_GAIADR3_EPOCH.csv"]
OUTPUT_CSV = "arithmetic_verified.csv"
LOG_FILE = "arithmetic_pipeline_log.txt"
CHUNK_SIZE = int(20000)  # adjust to available RAM
# ==============

log_lines = []

def log(msg: str):
    print(msg)
    log_lines.append(msg)

# --- Robust parser for a-invariants field ---
def parse_a_invariants_field(s: Any) -> Optional[List[int]]:
    """
    Accepts strings like:
      "[0,0,0,-31017,2102590]"
      "0,0,0,-31017,2102590"
      " [ 0 , 0 , 0 , -84 , 784 ] "
    Returns list of five ints or None if unparsable.
    """
    if s is None:
        return None
    if isinstance(s, (list, tuple)):
        # already parsed
        try:
            vals = [int(x) for x in s[:5]]
            if len(vals) == 5:
                return vals
        except Exception:
            return None
    # coerce to str
    try:
        st = str(s).strip()
    except Exception:
        return None
    if st == "" or st.lower() in {"nan", "none", "null"}:
        return None
    # remove surrounding quotes if present
    if (st.startswith('"') and st.endswith('"')) or (st.startswith("'") and st.endswith("'")):
        st = st[1:-1].strip()
    # if looks like python list, use ast.literal_eval
    if st.startswith("[") and st.endswith("]"):
        try:
            obj = ast.literal_eval(st)
            if isinstance(obj, (list, tuple)) and len(obj) >= 5:
                return [int(obj[i]) for i in range(5)]
        except Exception:
            pass
    # otherwise split by comma or whitespace
    sep_candidates = [",", ";", " "]
    for sep in sep_candidates:
        if sep in st:
            parts = [p.strip() for p in st.split(sep) if p.strip() != ""]
            if len(parts) >= 5:
                try:
                    return [int(parts[i]) for i in range(5)]
                except Exception:
                    # try float->int
                    try:
                        return [int(float(parts[i])) for i in range(5)]
                    except Exception:
                        pass
    # last resort: extract integers with simple scanning
    import re
    ints = re.findall(r"-?\d+", st)
    if len(ints) >= 5:
        try:
            return [int(ints[i]) for i in range(5)]
        except Exception:
            pass
    return None

# --- Exact algebraic invariants from a-invariants ---
def compute_b_and_discriminant(a1: int, a2: int, a3: int, a4: int, a6: int) -> dict:
    """
    Returns dict with b2,b4,b6,b8,c4,Delta (Fraction), j (Fraction or None)
    Uses exact Fraction arithmetic.
    """
    a1f, a2f, a3f, a4f, a6f = map(Fraction, (a1, a2, a3, a4, a6))
    b2 = a1f*a1f + 4*a2f
    b4 = a1f*a3f + 2*a4f
    b6 = a3f*a3f + 4*a6f
    b8 = a1f*a1f*a6f + 4*a2f*a6f - a1f*a3f*a4f + a2f*a3f*a3f - a4f*a4f
    # discriminant
    Delta = -b2*b2*b8 - 8*b4**3 - 27*b6**2 + 9*b2*b4*b6
    c4 = b2*b2 - 24*b4
    j = None
    if Delta != 0:
        j = (c4**3) / Delta
    return {
        "b2": b2, "b4": b4, "b6": b6, "b8": b8,
        "c4": c4, "Delta": Delta, "j": j
    }

# --- Safe CSV chunk reader that yields DataFrame or None if missing ---
def load_csv_if_exists(basename: str, chunksize: Optional[int] = None) -> Optional[pd.DataFrame]:
    path = os.path.join(DATA_DIR, basename)
    if not os.path.exists(path):
        log(f"File not found: {basename}")
        return None
    try:
        if chunksize is None:
            df = pd.read_csv(path, dtype=str)
            log(f"Loaded {basename}: {len(df)} rows, {len(df.columns)} columns.")
            return df
        else:
            # read in chunks and concat (memory safe for moderate sizes)
            chunks = []
            for ch in pd.read_csv(path, dtype=str, chunksize=chunksize):
                chunks.append(ch)
            df = pd.concat(chunks, ignore_index=True)
            log(f"Loaded {basename} in chunks: {len(df)} rows, {len(df.columns)} columns.")
            return df
    except Exception as e:
        log(f"Error reading {basename}: {e}")
        return None

# === Main pipeline ===
def main():
    log("Starting pipeline.")
    # load primary and optional tables
    primary = load_csv_if_exists(PRIMARY, chunksize=CHUNK_SIZE)
    parsed = load_csv_if_exists(PARSed, chunksize=CHUNK_SIZE)
    sel_lmfdb = load_csv_if_exists(SEL3_LMFDB, chunksize=CHUNK_SIZE)
    sel_crem = load_csv_if_exists(SEL3_CREM, chunksize=CHUNK_SIZE)
    other_dfs = {}
    for f in OTHER_FILES:
        df = load_csv_if_exists(f, chunksize=CHUNK_SIZE)
        if df is not None:
            other_dfs[f] = df

    if primary is None:
        log("Primary Cremona CSV not found. Exiting.")
        with open(LOG_FILE, "w") as lf:
            lf.write("\n".join(log_lines))
        sys.exit(1)

    # ensure label column exists
    if 'label' not in primary.columns:
        # try common alternatives
        for alt in ['Label', 'curve_label', 'name', 'id']:
            if alt in primary.columns:
                primary = primary.rename(columns={alt: 'label'})
                break
    if 'label' not in primary.columns:
        primary['label'] = [f"row_{i}" for i in range(len(primary))]

    # prepare output columns
    out_cols = list(primary.columns) + [
        'a1','a2','a3','a4','a6',
        'b2','b4','b6','b8','c4',
        'Delta_exact','Delta_float','j_exact','j_float',
        # placeholders for Sage-only fields
        'conductor','rank','regulator','tamagawa_product','tamagawa_dict',
        'torsion_order','real_period','selmer2','selmer3',
        'verification_flag','notes'
    ]
    # initialize output DataFrame
    out_df = primary.copy()
    for c in out_cols:
        if c not in out_df.columns:
            out_df[c] = None

    # parse and compute per row
    n = len(out_df)
    log(f"Processing {n} rows to compute discriminant and j.")
    for i, row in out_df.iterrows():
        label = str(row.get('label'))
        notes = []
        # parse a-invariants
        raw = row.get('used_a_invariants') if 'used_a_invariants' in out_df.columns else None
        a_parsed = parse_a_invariants_field(raw)
        if a_parsed is None:
            # try to find in parsed table by label
            if parsed is not None and 'label' in parsed.columns:
                match = parsed[parsed['label'].astype(str) == label]
                if len(match) >= 1 and 'used_a_invariants' in match.columns:
                    a_parsed = parse_a_invariants_field(match.iloc[0]['used_a_invariants'])
        if a_parsed is None:
            notes.append("a_invariants_missing_or_malformed")
            out_df.at[i, 'verification_flag'] = False
            out_df.at[i, 'notes'] = ";".join(notes)
            continue
        # store a_i
        a1,a2,a3,a4,a6 = a_parsed[:5]
        out_df.at[i,'a1'] = a1
        out_df.at[i,'a2'] = a2
        out_df.at[i,'a3'] = a3
        out_df.at[i,'a4'] = a4
        out_df.at[i,'a6'] = a6
        # compute invariants
        try:
            res = compute_b_and_discriminant(a1,a2,a3,a4,a6)
            out_df.at[i,'b2'] = str(res['b2'])
            out_df.at[i,'b4'] = str(res['b4'])
            out_df.at[i,'b6'] = str(res['b6'])
            out_df.at[i,'b8'] = str(res['b8'])
            out_df.at[i,'c4'] = str(res['c4'])
            out_df.at[i,'Delta_exact'] = str(res['Delta'])
            try:
                out_df.at[i,'Delta_float'] = float(res['Delta'])
            except Exception:
                out_df.at[i,'Delta_float'] = None
            out_df.at[i,'j_exact'] = str(res['j']) if res['j'] is not None else None
            out_df.at[i,'j_float'] = float(res['j']) if res['j'] is not None else None
            # mark verification flag: True for algebraic invariants computed
            out_df.at[i,'verification_flag'] = True
        except Exception as e:
            notes.append(f"compute_error:{e}")
            out_df.at[i,'verification_flag'] = False
        # mark Sage-required fields as missing (user can run in Sage later)
        out_df.at[i,'conductor'] = None
        out_df.at[i,'rank'] = None
        out_df.at[i,'regulator'] = None
        out_df.at[i,'tamagawa_product'] = None
        out_df.at[i,'tamagawa_dict'] = None
        out_df.at[i,'torsion_order'] = None
        out_df.at[i,'real_period'] = None
        out_df.at[i,'selmer2'] = None
        out_df.at[i,'selmer3'] = None
        if notes:
            out_df.at[i,'notes'] = ";".join(notes)

    # optional: merge selmer tables if present (by label)
    if sel_lmfdb is not None:
        if 'label' in sel_lmfdb.columns:
            # prefer sel_lmfdb columns named like label, selmer3 etc.
            sel_map = sel_lmfdb.set_index(sel_lmfdb['label'].astype(str))
            # join for rows present
            for i, row in out_df.iterrows():
                lab = str(row['label'])
                if lab in sel_map.index:
                    r = sel_map.loc[lab]
                    # if multiple matches, take first
                    if isinstance(r, pd.DataFrame):
                        r = r.iloc[0]
                    # copy known selmer fields if present
                    for col in ['selmer3','selmer2','3selmer','2selmer']:
                        if col in r.index and pd.notna(r[col]):
                            out_df.at[i,'selmer3'] = r[col]
    if sel_crem is not None:
        if 'label' in sel_crem.columns:
            sel_map = sel_crem.set_index(sel_crem['label'].astype(str))
            for i, row in out_df.iterrows():
                lab = str(row['label'])
                if lab in sel_map.index:
                    r = sel_map.loc[lab]
                    if isinstance(r, pd.DataFrame):
                        r = r.iloc[0]
                    for col in ['selmer3','selmer2','3selmer','2selmer']:
                        if col in r.index and pd.notna(r[col]) and out_df.at[i,'selmer3'] is None:
                            out_df.at[i,'selmer3'] = r[col]

    # final write
    out_df.to_csv(os.path.join(DATA_DIR, OUTPUT_CSV), index=False)
    log(f"Wrote output to {OUTPUT_CSV}")

    # write log
    with open(os.path.join(DATA_DIR, LOG_FILE), "w") as lf:
        lf.write("\n".join(log_lines))
    log(f"Wrote log to {LOG_FILE}")
    # summary
    total = len(out_df)
    verified = out_df['verification_flag'].astype(bool).sum()
    log(f"Summary: {total} rows processed; {verified} rows have algebraic invariants computed; remaining rows need manual/Sage processing.")
    log("Fields requiring Sage/PARI for completion: conductor, rank, regulator, tamagawa, torsion, real_period, selmer groups.")
    log("To compute those, run this script inside Sage's python or call sagelib and replace the Sage branch accordingly.")

if __name__ == "__main__":
    main()
