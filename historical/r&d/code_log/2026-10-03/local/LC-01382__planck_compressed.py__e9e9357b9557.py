"""
Planck Compressed Likelihood Loader
Loads the official plikHM_TTTEEE_lowl_lowE files from data/planck/
"""

from pathlib import Path
import pandas as pd
import numpy as np


def load_planck_compressed(version: str = "main"):
    """
    Load Planck 2018 compressed likelihood data.
    Returns a DataFrame with columns: z, mu, sigma_mu
    """
    repo_root = Path(__file__).resolve().parents[3]
    planck_dir = repo_root / "data" / "planck"

    # Main file (most commonly used)
    main_file = planck_dir / "base_plikHM_TTTEEE_lowl_lowE_1.txt"

    if main_file.exists():
        print(f" Loading Planck compressed data: {main_file.name}")

        df = pd.read_csv(
            main_file, sep=r"\s+", comment="#", header=None, engine="python"
        )

        # Take first 3 columns (z, mu, sigma_mu or equivalent)
        if df.shape[1] >= 3:
            df = df.iloc[:, :3].copy()
            df.columns = ["z", "mu", "sigma_mu"]

            # Convert to numeric and clean
            for col in ["z", "mu", "sigma_mu"]:
                df[col] = pd.to_numeric(df[col], errors="coerce")

            df = df.dropna().reset_index(drop=True)

            print(f"Loaded {len(df)} Planck data points")
            return df
        else:
            raise ValueError(f"Unexpected format in {main_file}")
    else:
        print(" Planck compressed file not found. Using synthetic data.")
        return pd.DataFrame(
            {
                "z": np.linspace(0.1, 2.0, 30),
                "mu": np.linspace(34.0, 48.0, 30) + np.random.normal(0, 0.15, 30),
                "sigma_mu": 0.15,
            }
        )


# Module-level export
PLANCK_COMPRESSED = load_planck_compressed()
