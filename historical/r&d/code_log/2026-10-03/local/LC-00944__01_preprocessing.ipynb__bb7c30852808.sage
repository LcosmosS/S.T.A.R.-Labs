import json, re, time
from pathlib import Path
import numpy as np
import pandas as pd

RAW_CSV = "cremona_raw_parsed.csv"          # or lmfdb_raw_parsed.csv
CLEAN_CSV = "acsc_validation_cremona.csv"   # output
MANIFEST = CLEAN_CSV.replace(".csv", ".manifest.json")

# canonical column mapping
CANONICAL = {
    "delta": ["delta","minimal_discriminant","disc","D","discriminant"],
    "conductor": ["conductor","N","cond","label"],
    "rank": ["sage_rank","rank","algebraic_rank","pari_analytic_rank"],
    "regulator": ["regulator","R"],
    "real_period": ["real_period","omega_real","Q"],
    "torsion_order": ["torsion_order","torsion","T"],
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
    col_matches = {k: find_col(df, v) for k,v in CANONICAL.items()}
    out = pd.DataFrame(index=df.index)

    # fill canonical columns
    for key, col in col_matches.items():
        out[key] = df[col] if col is not None else np.nan

    # conductor fallback
    if col_matches.get("conductor") is None and "label" in df.columns:
        out["conductor"] = df["label"].apply(extract_conductor_from_label)

    # numeric coercion
    for c in ["delta","conductor","rank","regulator","real_period","torsion_order"]:
        out[c] = pd.to_numeric(out[c], errors="coerce")

    # keep label + source if present
    for extra in ["label","source"]:
        if extra in df.columns:
            out[extra] = df[extra]

    diag = {
        "rows_total": int(len(df)),
        "col_matches": col_matches,
        "null_counts": {k:int(v) for k,v in out.isna().sum().to_dict().items()}
    }
    return out, diag

def reprocess_file(infile, outfile, manifest_path):
    infile = Path(infile)
    outfile = Path(outfile)
    manifest_path = Path(manifest_path)

    df = pd.read_csv(infile)
    cleaned, diag = normalize_and_clean_df(df)

    # ACSC policy: require delta + rank
    mask = cleaned["delta"].notna() & cleaned["rank"].notna()
    kept = cleaned[mask].copy()

    kept.to_csv(outfile, index=False)

    manifest = {
        "input_file": str(infile),
        "output_file": str(outfile),
        "rows_input": int(len(df)),
        "rows_output": int(len(kept)),
        "diagnostics": diag,
        "drop_policy": "drop rows missing delta or rank",
        "timestamp": time.time()
    }
    manifest_path.write_text(json.dumps(manifest, indent=2))
    print(f"Wrote cleaned CSV {outfile} rows_out={len(kept)}")
    return kept, manifest

clean_df, manifest = reprocess_file(RAW_CSV, CLEAN_CSV, MANIFEST)
clean_df.head()

from acsc.projection import project as project_primary
from acsc.alt_mappings import map_ptd, map_mcj

records = clean_df.to_dict(orient="records")

coords_primary = project_primary(records, method="primary", Amax=1.0, Nmax=1.0, V0=1.0)
coords_ptd     = map_ptd(records, Amax=1.0, Nmax=1.0, V0=1.0)
coords_mcj     = map_mcj(records, Amax=1.0, Nmax=1.0, V0=1.0)

clean_df[["x_prim","y_prim","z_prim"]] = coords_primary
clean_df[["x_ptd","y_ptd","z_ptd"]] = coords_ptd
clean_df[["x_mcj","y_mcj","z_mcj"]] = coords_mcj

clean_df.to_csv("derived/acsc_projected_cremona.csv", index=False)
print("Wrote derived/acsc_projected_cremona.csv")

from acsc.quantile import QuantileAligner

aligner = QuantileAligner()
ref = clean_df[["x_prim","y_prim","z_prim"]].sample(5000, random_state=int(42)).to_numpy()
aligner.fit(ref, n_quantiles=200)

aligned = aligner.transform(clean_df[["x_prim","y_prim","z_prim"]].to_numpy())
clean_df[["x_al","y_al","z_al"]] = aligned

clean_df.to_csv("derived/acsc_projected_cremona_aligned.csv", index=False)
print("Wrote aligned projection")

print("Rows:", len(clean_df))
print("Null counts:", clean_df.isna().sum().to_dict())
print("Conductor range:", clean_df["conductor"].min(), clean_df["conductor"].max())
print("Delta range:", clean_df["delta"].min(), clean_df["delta"].max())
clean_df.sample(5, random_state=int(42))
