"""Fail-closed loader for a local Planck compressed-likelihood artifact."""

from pathlib import Path

import pandas as pd


def load_planck_compressed(version: str = "main"):
    """Load the configured Planck compressed-likelihood table.

    Missing source data is an execution error. No synthetic observational
    replacement is generated.
    """
    if version != "main":
        raise ValueError(f"unsupported Planck compressed version: {version}")

    repo_root = Path(__file__).resolve().parents[3]
    main_file = repo_root / "data" / "planck" / "base_plikHM_TTTEEE_lowl_lowE_1.txt"

    if not main_file.exists():
        raise FileNotFoundError(
            "Planck compressed source is missing: "
            f"{main_file}. Synthetic fallback data is forbidden."
        )

    df = pd.read_csv(
        main_file,
        sep=r"\s+",
        comment="#",
        header=None,
        engine="python",
    )
    if df.shape[1] < 3:
        raise ValueError(f"Unexpected format in {main_file}")

    df = df.iloc[:, :3].copy()
    df.columns = ["z", "mu", "sigma_mu"]
    for col in ("z", "mu", "sigma_mu"):
        df[col] = pd.to_numeric(df[col], errors="coerce")

    if df.isna().any().any():
        raise ValueError(f"Non-numeric or missing values found in {main_file}")
    if df.empty:
        raise ValueError(f"Planck compressed source is empty: {main_file}")
    if (df["sigma_mu"] <= 0).any():
        raise ValueError("Planck compressed uncertainties must be positive")
    return df.reset_index(drop=True)


PLANCK_COMPRESSED = load_planck_compressed()
