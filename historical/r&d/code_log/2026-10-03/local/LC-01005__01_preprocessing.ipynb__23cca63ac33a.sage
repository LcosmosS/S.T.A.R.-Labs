# Notebook cell: end-to-end small pipeline
import json, re, os
from pathlib import Path
import pandas as pd
import numpy as np
from datetime import datetime

# imports from your package
from acsc.projection import project as project_records

# helper functions (reprocessor + merge)
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
    if pd.isna(label): return None
    s = str(label).strip()
    m = re.match(r"^\s*(\d+)", s)
    if m: return int(m.group(1))
    m = re.match(r"^(\d+)\.", s)
    if m: return int(m.group(1))
    return None

def normalize_and_clean_df(df):
    col_matches = {k: find_col(df, v) for k,v in CANONICAL.items()}
    out = pd.DataFrame(index=df.index)
    for key,col in col_matches.items():
        out[key] = df[col] if col is not None else pd.NA
    if col_matches.get("conductor") is None and "label" in df.columns:
        out["conductor"] = df["label"].apply(extract_conductor_from_label)
    for c in ["delta","conductor","rank","regulator","real_period","torsion_order"]:
        out[c] = pd.to_numeric(out[c], errors="coerce")
    for extra in ["label","source"]:
        if extra in df.columns:
            out[extra] = df[extra]
    return out

def reprocess_and_merge(infile, lookup_csv, out_csv):
    df = pd.read_csv(infile)
    cleaned = normalize_and_clean_df(df)
    kept = cleaned[cleaned["delta"].notna() & cleaned["rank"].notna()].copy()
    if Path(lookup_csv).exists():
        lookup = pd.read_csv(lookup_csv)
        merged = kept.merge(lookup, on="label", how="left", suffixes=("","_lk"))
        for col in ["regulator","real_period","torsion_order","conductor"]:
            lk = col + "_lk"
            if lk in merged.columns:
                merged[col] = merged[col].fillna(merged[lk])
                merged = merged.drop(columns=[lk])
    else:
        merged = kept
    Path(out_csv).parent.mkdir(parents=True, exist_ok=True)
    merged.to_csv(out_csv, index=False)
    print("Wrote cleaned+merged", out_csv, "rows:", len(merged))
    return merged

# Paths (edit as needed)
lookup = "data/arith_lookup_by_label.csv"
crem_in = "cremona_raw_parsed.csv"
crem_out = "derived/acsc_projected_cremona_final.csv"

# Run reprocess+merge
df_final = reprocess_and_merge(crem_in, lookup, crem_out.replace(".csv", ".cleaned.csv"))

# Project and attach coords
records = df_final.to_dict(orient="records")
coords_primary = project_records(records, method="primary", Amax=Amax, Nmax=Nmax, V0=V0)
coords_ptd     = project_records(records, method="ptd")
coords_mcj     = project_records(records, method="mcj")
df_final[["x_prim","y_prim","z_prim"]] = coords_primary
df_final[["x_ptd","y_ptd","z_ptd"]] = coords_ptd
df_final[["x_mcj","y_mcj","z_mcj"]] = coords_mcj

# Save final derived CSV and manifest
out_csv = crem_out
df_final.to_csv(out_csv, index=False)
manifest = {
  "created_at": datetime.utcnow().isoformat() + "Z",
  "rows_output": int(len(df_final)),
  "notes": "reprocessed, merged lookup, projected"
}
Path(out_csv + ".manifest.json").write_text(json.dumps(manifest, indent=2))
print("Wrote final derived CSV and manifest:", out_csv)
display(df_final.head(int(3)))
