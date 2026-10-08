#!/usr/bin/env python3
"""
Pantheon+ Preprocessing Script
Downloads pantheon_plus.dat (or uses local copy),
extracts z, mu, sigma_mu, and writes a clean Python dict
to src/likelihoods/data/pantheon_plus_full.py
"""

import pandas as pd
from pathlib import Path

RAW = Path("data/processed/pantheon_plus.csv")
OUT = Path("src/likelihoods/data/pantheon_plus_full.py")

def main():
    if not RAW.exists():
        raise FileNotFoundError(
            f"{RAW} not found. Place pantheon_plus.csv in data/processed/"
        )

    print(f"Loading Pantheon+ from {RAW} ...")
    df = pd.read_csv(RAW, delim_whitespace=True, comment="#", header=0)

    # Column mapping
    rename_map = {
        "zHD": "z",
        "zCMB": "z",
        "m_b_corr": "mu",
        "MU_SH0ES": "mu",
        "m_b_corr_err_DIAG": "sigma_mu",
        "MU_SH0ES_ERR_DIAG": "sigma_mu",
        "dmu": "sigma_mu",
    }
    df = df.rename(columns=rename_map)

    # Force required columns
    if "z" not in df.columns:
        df["z"] = df.get("zHD", df.get("zCMB"))
    if "mu" not in df.columns:
        df["mu"] = df.get("m_b_corr", df.get("MU_SH0ES"))
    if "sigma_mu" not in df.columns:
        df["sigma_mu"] = df.get("m_b_corr_err_DIAG",
                                df.get("MU_SH0ES_ERR_DIAG"))

    # Drop rows missing required fields
    df = df[["z", "mu", "sigma_mu"]].dropna()

    print(f"Final Pantheon+ sample size: {len(df)} SNe")

    # Convert to Python lists
    z = df["z"].tolist()
    mu = df["mu"].tolist()
    sigma = df["sigma_mu"].tolist()

    # Write Python module
    OUT.parent.mkdir(parents=True, exist_ok=True)
    with open(OUT, "w") as f:
        f.write("# Auto-generated Pantheon+ full sample\n")
        f.write("# Do not edit manually.\n\n")
        f.write("PANTHEON_PLUS_FULL = {\n")
        f.write(f"    'z': {z},\n")
        f.write(f"    'mu': {mu},\n")
        f.write(f"    'sigma_mu': {sigma},\n")
        f.write("}\n")

    print(f"Wrote cleaned dataset to {OUT}")

if __name__ == "__main__":
    main()
