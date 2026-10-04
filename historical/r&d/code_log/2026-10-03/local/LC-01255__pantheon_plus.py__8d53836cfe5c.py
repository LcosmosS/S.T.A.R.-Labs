"""
Robust Pantheon+ Loader and module export.
Produces PANTHEON_PLUS_FULL as a dict of lists:
{
  "z": [...],
  "mu": [...],
  "sigma_mu": [...]
}
"""

"""
Pantheon+ Loader - Returns pandas DataFrame directly (most reliable)
"""
from pathlib import Path
import pandas as pd
import numpy as np


def load_pantheon_plus():
    repo_root = Path(__file__).resolve().parents[3]
    csv_path = repo_root / "data" / "processed" / "pantheon_plus.csv"

    if csv_path.exists():
        df = pd.read_csv(csv_path)

        # Clean any remaining weird values
        df = df.replace(["...", "... ", -999, -999.0], np.nan)

        # Normalize columns if needed
        rename_map = {
            "zHD": "z",
            "zCMB": "z",
            "m_b_corr": "mu",
            "m_b_corr_err_DIAG": "sigma_mu",
            "MU_SH0ES": "mu",
        }
        df = df.rename(columns=rename_map)

        required = ["z", "mu", "sigma_mu"]
        for col in required:
            if col not in df.columns:
                df[col] = np.nan
            df[col] = pd.to_numeric(df[col], errors="coerce")

        df = df.dropna(subset=["z", "mu"]).reset_index(drop=True)

        print(f" Loaded {len(df)} Pantheon+ supernovae from processed CSV")
        return df  # ← Return DataFrame directly

    else:
        print(" CSV not found - using placeholder")
        return pd.DataFrame(
            {"z": [0.01, 0.05], "mu": [32.5, 35.0], "sigma_mu": [0.08, 0.10]}
        )


# Export
PANTHEON_PLUS_FULL = load_pantheon_plus()
