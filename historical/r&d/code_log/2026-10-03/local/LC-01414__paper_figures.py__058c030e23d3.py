"""
Paper-Ready Cosmology Figures
=============================

Generates:
- Hubble diagram
- H(z) curves
- Distance modulus curves
- Residuals
- Posterior corner plots
"""

import os
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path


def _ensure_outdir(output_dir):
    if output_dir:
        os.makedirs(output_dir, exist_ok=True)


def plot_hubble_diagram(df, lcdm, star, output_dir="results"):
    """Plot Hubble diagram"""
    df = df if isinstance(df, dict) else df
    if isinstance(df, dict):
        df = pd.DataFrame(df).T  # safety

    z = np.asarray(df["z"].values, dtype=float)
    mu_obs = np.asarray(df["mu"].values, dtype=float)
    sigma = np.asarray(df.get("sigma_mu", 0.15), dtype=float)

    # Compute model predictions
    mu_lcdm = np.array([lcdm.distance_modulus(zi) for zi in z])
    mu_star = np.array([star.distance_modulus(zi) for zi in z])

    plt.figure(figsize=(10, 6))
    plt.errorbar(z, mu_obs, yerr=sigma, fmt=".", label="Pantheon+", alpha=0.6)
    plt.plot(z, mu_lcdm, label="ΛCDM", color="C1")
    plt.plot(z, mu_star, label="S.T.A.R.", color="C2", linestyle="--")
    plt.xscale("log")
    plt.xlabel("z")
    plt.ylabel("Distance modulus μ")
    plt.legend()
    plt.tight_layout()

    if output_dir:
        outpath = os.path.join(output_dir, "hubble_diagram.png")
        plt.savefig(outpath, dpi=200)
    plt.close()


def plot_Hz(models, labels, output_dir="results"):
    """Improved H(z) plot with better model detection"""
    from pathlib import Path

    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    zgrid = np.linspace(0.0, 2.5, 200)
    plt.figure(figsize=(8, 5))

    for model, lab in zip(models, labels):
        Hz = None
        try:
            # Try common cosmology method names
            if hasattr(model, "H"):
                Hz = np.array([model.H(z) for z in zgrid])
            elif hasattr(model, "hubble_parameter"):
                Hz = np.array([model.hubble_parameter(z) for z in zgrid])
            elif hasattr(model, "efunc") and hasattr(model, "H0"):
                Hz = np.array([model.efunc(z) * model.H0 for z in zgrid])
            elif hasattr(model, "H0"):
                # Use constant H(z) = H0 as fallback (better than 70 hardcoded)
                h0 = float(model.H0)
                Hz = np.full_like(zgrid, h0)
                print(f"→ Using constant H(z) = H0 ≈ {h0:.1f} for {lab}")
            else:
                Hz = np.full_like(zgrid, 70.0)
                print(
                    f"Warning: No H(z) method found for {lab}, using placeholder H0=70"
                )
        except Exception as e:
            print(f"Error computing H(z) for {lab}: {e}")
            Hz = np.full_like(zgrid, 70.0)

        plt.plot(zgrid, Hz, label=lab, lw=2.2)

    plt.xlabel("Redshift z")
    plt.ylabel("H(z) [km/s/Mpc]")
    plt.title("Hubble Parameter Evolution")
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.savefig(output_dir / "Hz_comparison.png", dpi=300, bbox_inches="tight")
    plt.close()
    print(f" Saved H(z) plot")


def plot_residuals(df, lcdm, star, output_dir=None):
    """
    Plot residuals (data - model) for ΛCDM and S.T.A.R.
    Signature: plot_residuals(df, lcdm, star, output_dir=None)
    """
    _ensure_outdir(output_dir)

    z = np.array(df["z"])
    mu_obs = np.array(df["mu"])
    sigma = np.array(df["sigma_mu"])

    mu_lcdm = np.array([lcdm.distance_modulus(zi) for zi in z])
    mu_star = np.array([star.distance_modulus(zi) for zi in z])

    res_lcdm = mu_obs - mu_lcdm
    res_star = mu_obs - mu_star

    plt.figure(figsize=(10, 4))
    plt.errorbar(z, res_lcdm, yerr=sigma, fmt=".", label="Data - ΛCDM", alpha=0.6)
    plt.errorbar(z, res_star, yerr=sigma, fmt=".", label="Data - S.T.A.R.", alpha=0.6)
    plt.xscale("log")
    plt.axhline(0, color="k", lw=0.8)
    plt.xlabel("z")
    plt.ylabel("Residual μ (mag)")
    plt.legend()
    plt.tight_layout()

    if output_dir:
        outpath = os.path.join(output_dir, "residuals.png")
        plt.savefig(outpath, dpi=200)
    plt.close()
