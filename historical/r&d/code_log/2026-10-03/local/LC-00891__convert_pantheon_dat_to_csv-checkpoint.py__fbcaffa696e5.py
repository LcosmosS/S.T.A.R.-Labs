from pathlib import Path
import pandas as pd
import sys

RAW = Path("data/raw/pantheon_plus.dat")
OUT_DIR = Path("data/processed")
OUT = OUT_DIR / "pantheon_plus.csv"

if not RAW.exists():
    print(f"Error: {RAW} not found. Place the Pantheon+ .dat file in data/raw/", file=sys.stderr)
    sys.exit(1)

# Read using regex whitespace separator (robust to variable spacing)
df = pd.read_csv(RAW, sep=r'\s+', comment="#", header=0, engine="python")

# Map common column names to canonical names used by your pipeline
rename_map = {
    "zHD": "z", "zCMB": "z", "zHEL": "z",
    "m_b_corr": "mu", "MU_SH0ES": "mu",
    "m_b_corr_err_DIAG": "sigma_mu", "MU_SH0ES_ERR_DIAG": "sigma_mu",
    "dmu": "sigma_mu"
}
df = df.rename(columns=rename_map)

# Collapse duplicate columns that may have been renamed to the same key
def collapse_duplicates(df, key):
    cols = [c for c in df.columns if c == key]
    if not cols:
        return None
    if len(cols) == 1:
        return df[cols[0]]
    sub = df[cols]
    return sub.bfill(axis=1).iloc[:, 0]

z = collapse_duplicates(df, "z")
mu = collapse_duplicates(df, "mu")
sigma = collapse_duplicates(df, "sigma_mu")

# Fallbacks if collapse found nothing
if z is None:
    for alt in ("zHD", "zCMB", "zHEL"):
        if alt in df.columns:
            z = df[alt]; break
if mu is None:
    for alt in ("m_b_corr", "MU_SH0ES"):
        if alt in df.columns:
            mu = df[alt]; break
if sigma is None:
    for alt in ("m_b_corr_err_DIAG", "MU_SH0ES_ERR_DIAG", "dmu"):
        if alt in df.columns:
            sigma = df[alt]; break

if z is None or mu is None or sigma is None:
    print("Error: required columns (z, mu, sigma_mu) not found after parsing.", file=sys.stderr)
    print("Available columns:", list(df.columns), file=sys.stderr)
    sys.exit(2)

clean = pd.DataFrame({"z": z, "mu": mu, "sigma_mu": sigma})

# Coerce to numeric and drop rows with invalid values
clean = clean.replace([None, ""], pd.NA)
for col in ["z", "mu", "sigma_mu"]:
    clean[col] = pd.to_numeric(clean[col], errors="coerce")
clean = clean.dropna().reset_index(drop=True)

# Optional: sort by redshift
clean = clean.sort_values("z").reset_index(drop=True)

OUT_DIR.mkdir(parents=True, exist_ok=True)
clean.to_csv(OUT, index=False)
print(f"Wrote {OUT} with {len(clean)} rows")
