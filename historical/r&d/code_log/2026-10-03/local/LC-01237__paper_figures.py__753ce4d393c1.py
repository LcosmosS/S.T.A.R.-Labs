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

from __future__ import annotations
import numpy as np
import matplotlib.pyplot as plt
import corner


def plot_hubble_diagram(df, lcdm, star):
    z = df["z"].values
    mu_obs = df["mu"].values
    sigma = df["sigma_mu"].values

    mu_lcdm = np.array([lcdm.distance_modulus(zi) for zi in z])
    mu_star = np.array([star.distance_modulus(zi) for zi in z])

    plt.figure(figsize=(10,6))
    plt.errorbar(z, mu_obs, sigma, fmt="o", label="Data", alpha=0.6)
    plt.plot(z, mu_lcdm, label="ΛCDM", lw=2)
    plt.plot(z, mu_star, label="S.T.A.R.", lw=2)
    plt.xlabel("Redshift z")
    plt.ylabel("Distance Modulus μ")
    plt.legend()
    plt.grid()
    plt.tight_layout()
    plt.show()


def plot_Hz(models, labels, zmax=2):
    z = np.linspace(0, zmax, 200)
    plt.figure(figsize=(10,6))
    for model, label in zip(models, labels):
        H = np.array([model.H(zi) for zi in z])
        plt.plot(z, H, label=label, lw=2)
    plt.xlabel("z")
    plt.ylabel("H(z)")
    plt.legend()
    plt.grid()
    plt.tight_layout()
    plt.show()


def plot_residuals(df, lcdm, star):
    z = df["z"].values
    mu_obs = df["mu"].values

    mu_lcdm = np.array([lcdm.distance_modulus(zi) for zi in z])
    mu_star = np.array([star.distance_modulus(zi) for zi in z])

    plt.figure(figsize=(10,4))
    plt.scatter(z, mu_obs - mu_lcdm, s=10, label="Obs - ΛCDM")
    plt.scatter(z, mu_obs - mu_star, s=10, label="Obs - S.T.A.R.")
    plt.axhline(0, color="black", lw=1)
    plt.xlabel("z")
    plt.ylabel("Residual μ")
    plt.legend()
    plt.grid()
    plt.tight_layout()
    plt.show()


def plot_corner(chain, labels):
    fig = corner.corner(chain, labels=labels, show_titles=True)
    fig.tight_layout()
    return fig
