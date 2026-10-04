"""
Hubble Diagram Visualization
============================

Plots:
- Observed distance modulus vs redshift
- ΛCDM prediction
- S.T.A.R. Model prediction
- Residuals

Used to visualize the Hubble–Planck tension.
"""

from __future__ import annotations
import numpy as np
import matplotlib.pyplot as plt


def plot_hubble_diagram(df, lcdm, star, zmax=0.2):
    """
    Parameters
    ----------
    df : DataFrame
        Must contain columns: redshift, mu_obs
    lcdm : Cosmology
    star : SymbolicCosmology
    """

    z = df["redshift"].values
    mu_obs = df["mu_obs"].values

    mu_lcdm = np.array([lcdm.distance_modulus(zi) for zi in z])
    mu_star = np.array([star.distance_modulus(zi) for zi in z])

    plt.figure(figsize=(10,6))
    plt.scatter(z, mu_obs, s=10, alpha=0.6, label="Observed")
    plt.plot(z, mu_lcdm, lw=2, label="ΛCDM")
    plt.plot(z, mu_star, lw=2, label="S.T.A.R. Model")
    plt.xlabel("Redshift z")
    plt.ylabel("Distance Modulus μ")
    plt.title("Hubble Diagram: Observations vs ΛCDM vs S.T.A.R.")
    plt.legend()
    plt.grid()
    plt.show()

    # Residuals
    plt.figure(figsize=(10,4))
    plt.scatter(z, mu_obs - mu_lcdm, s=10, alpha=0.6, label="Obs - ΛCDM")
    plt.scatter(z, mu_obs - mu_star, s=10, alpha=0.6, label="Obs - S.T.A.R.")
    plt.axhline(0, color="black", lw=1)
    plt.xlabel("Redshift z")
    plt.ylabel("Residual μ")
    plt.title("Residuals")
    plt.legend()
    plt.grid()
    plt.show()
