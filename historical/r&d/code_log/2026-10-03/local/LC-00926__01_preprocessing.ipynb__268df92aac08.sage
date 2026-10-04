# Notebook cell: reprocess without CLI
import json, re
from pathlib import Path
import pandas as pd
import numpy as np

CANONICAL = {
    "delta": ["delta", "minimal_discriminant", "disc", "D", "discriminant"],
    "conductor": ["conductor", "N", "cond", "label"],
    "rank": ["sage_rank", "rank", "algebraic_rank", "pari_analytic_rank"],
    "regulator": ["regulator", "R"],
    "real_period": ["real_period", "omega_real", "Q"],
    "torsion_order": ["torsion_order", "torsion", "T"],
}

def find_col(df, candidates):
    for c in candidates:
        if c in df.columns:
            return c
    return None

def extract_conductor_from_label(label):
    if pd.isna(label):
        return None
    s = str(label).strip()
    m = re.match(r"^\s*(\d+)", s)
    if m:
        return int(m.group(1))
    m = re.match(r"^(\d+)\.", s)
    if m:
        return int(m.group(1))
    return None

def normalize_and_clean_df(df):
    col_matches = {k: find_col(df, v) for k, v in CANONICAL.items()}
    out = pd.DataFrame(index=df.index)
    for key, col in col_matches.items():
        out[key] = df[col] if col is not None else np.nan
    if col_matches.get("conductor") is None and "label" in df.columns:
        out["conductor"] = df["label"].apply(extract_conductor_from_label)
    for c in ["delta","conductor","rank","regulator","real_period","torsion_order"]:
        out[c] = pd.to_numeric(out[c], errors="coerce")
    for extra in ["label","source"]:
        if extra in df.columns:
            out[extra] = df[extra]
    diag = {"rows_total": int(len(df)), "col_matches": col_matches, "null_counts": out.isna().sum().to_dict()}
    return out, diag

def reprocess_file(infile, outfile, manifest_path=None):
    infile = Path(infile)
    outfile = Path(outfile)
    manifest_path = Path(manifest_path) if manifest_path else outfile.with_suffix(".manifest.json")
    df = pd.read_csv(infile)
    cleaned, diag = normalize_and_clean_df(df)
    # policy: require delta and rank; keep rows that have both
    mask_keep = cleaned["delta"].notna() & cleaned["rank"].notna()
    kept = cleaned[mask_keep].copy()
    kept.to_csv(outfile, index=False)
    manifest = {
        "input_file": str(infile),
        "output_file": str(outfile),
        "rows_input": int(len(df)),
        "rows_output": int(len(kept)),
        "diagnostics": diag,
        "drop_policy": "drop rows missing delta or rank",
    }
    manifest_path.write_text(json.dumps(manifest, indent=2))
    print(f"Wrote cleaned CSV {outfile} rows_out {len(kept)}; manifest {manifest_path}")
    return kept, manifest

# Example usage: change paths to your files
crem_in = "cremona_raw_parsed.csv"
crem_out = "acsc_validation_cremona.csv"
lmf_in  = "lmfdb_raw_parsed.csv"
lmf_out = "acsc_validation_lmfdb.csv"

# Run reprocessing
for inp, outp in [(crem_in, crem_out), (lmf_in, lmf_out)]:
    if Path(inp).exists():
        kept_df, manifest = reprocess_file(inp, outp)
        display(kept_df.head(int(3)))
    else:
        print("Input not found:", inp)
