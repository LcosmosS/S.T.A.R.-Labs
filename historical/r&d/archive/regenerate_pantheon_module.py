"""
Regenerate a canonical, importable Pantheon+ module:
  src/likelihoods/data/pantheon_plus.py

The generated module exports:
  PANTHEON_PLUS_FULL = {"z": [...], "mu": [...], "sigma_mu": [...]}

This script:
- reads data/raw/pantheon_plus.dat
- maps common column names to canonical names
- collapses duplicate columns (takes first non-null per row)
- coerces to numeric and drops invalid rows
- writes a deterministic Python module with numeric lists
"""
from pathlib import Path
import pandas as pd
import sys

RAW = Path("data/raw/pantheon_plus.dat")
OUT = Path("src/likelihoods/data/pantheon_plus.py")  # canonical module

if not RAW.exists():
    print(f"Error: {RAW} not found. Place pantheon_plus.dat in data/raw/", file=sys.stderr)
    sys.exit(1)

# Read using regex separator (avoids deprecated delim_whitespace)
df = pd.read_csv(RAW, sep=r'\s+', comment="#", header=0, engine="python")

# Map many possible input names to canonical names
rename_map = {
    "zHD": "z", "zCMB": "z",
    "m_b_corr": "mu", "MU_SH0ES": "mu",
    "m_b_corr_err_DIAG": "sigma_mu", "MU_SH0ES_ERR_DIAG": "sigma_mu",
    "dmu": "sigma_mu"
}
df = df.rename(columns=rename_map)

# Collapse duplicate columns (if renaming produced multiple 'z' etc.)
def collapse_duplicates(df, target):
    cols = [c for c in df.columns if c == target]
    if len(cols) == 0:
        return None
    if len(cols) == 1:
        return df[cols[0]]
    sub = df[cols]
    # Backfill across columns and take first non-null per row
    collapsed = sub.bfill(axis=1).iloc[:, 0]
    return collapsed

z_series = collapse_duplicates(df, "z")
mu_series = collapse_duplicates(df, "mu")
sigma_series = collapse_duplicates(df, "sigma_mu")

# Fallback to original names if collapse found nothing
if z_series is None:
    for alt in ("zHD", "zCMB"):
        if alt in df.columns:
            z_series = df[alt]
            break
if mu_series is None:
    for alt in ("m_b_corr", "MU_SH0ES"):
        if alt in df.columns:
            mu_series = df[alt]
            break
if sigma_series is None:
    for alt in ("m_b_corr_err_DIAG", "MU_SH0ES_ERR_DIAG", "dmu"):
        if alt in df.columns:
            sigma_series = df[alt]
            break

if z_series is None or mu_series is None or sigma_series is None:
    print("Error: Could not find required columns (z, mu, sigma_mu) after parsing.", file=sys.stderr)
    print("Available columns:", list(df.columns), file=sys.stderr)
    sys.exit(2)

# Compose a cleaned DataFrame and coerce to numeric
clean_df = pd.DataFrame({
    "z": z_series,
    "mu": mu_series,
    "sigma_mu": sigma_series
})

# Drop rows with missing or non-numeric values
clean_df = clean_df.replace([None, ""], pd.NA).dropna()
for col in ["z", "mu", "sigma_mu"]:
    clean_df[col] = pd.to_numeric(clean_df[col], errors="coerce")
clean_df = clean_df.dropna()

# Final numeric conversion
clean_df = clean_df.astype(float)

# Debug prints for CI logs
print("DEBUG: clean_df shape:", clean_df.shape)
print("DEBUG: first 10 rows:")
print(clean_df.head(10).to_string(index=False))

z = clean_df["z"].tolist()
mu = clean_df["mu"].tolist()
sigma = clean_df["sigma_mu"].tolist()

OUT.parent.mkdir(parents=True, exist_ok=True)
with open(OUT, "w") as f:
    f.write("# Auto-generated Pantheon+ dataset (numeric lists)\n")
    f.write("# Do not edit manually. Regenerate with scripts/regenerate_pantheon_module.py\n\n")
    f.write("PANTHEON_PLUS_FULL = {\n")
    f.write(f"    'z': {z},\n")
    f.write(f"    'mu': {mu},\n")
    f.write(f"    'sigma_mu': {sigma}\n")
    f.write("}\n")

print('Wrote', OUT, 'with', len(z), 'SNe')
