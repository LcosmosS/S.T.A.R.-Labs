# 1. Imports
import sys
import os
from pathlib import Path

def get_project_root():
    # Case 1: Running under nbconvert or Jupyter (no __file__)
    if "__file__" not in globals():
        # Use the current working directory and walk upward until we find src/
        cwd = Path(os.getcwd()).resolve()
        for parent in [cwd] + list(cwd.parents):
            if (parent / "src").exists():
                return parent
        # Fallback: just use cwd
        return cwd

    # Case 2: Running as a script (normal Python)
    return Path(__file__).resolve().parents[1]

ROOT = get_project_root()
sys.path.insert(0, str(ROOT))
print("Project root added to sys.path:", ROOT)

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

from src.physics.cosmology import Cosmology
from src.physics.symbolic_cosmology import SymbolicCosmology
from src.physics.hubble_tension import compute_H0_tension
from src.physics.bayesian_model_comparison import (
    log_evidence_laplace, bayes_factor, jeffreys_scale
)

# 2. Load Planck distance priors (compressed likelihood)
planck = pd.read_csv("data/planck/planck_distance_priors.csv")
z = planck["z"].values
mu_obs = planck["mu"].values
sigma_mu = planck["sigma_mu"].values

# 3. Define ΛCDM
lcdm = Cosmology(
    "H0*sqrt(Ωm*(1+z)**3 + ΩΛ)",
    {"H0": 67.4, "Ωm": 0.315, "ΩΛ": 0.685}
)

# 4. Define S.T.A.R. Model (example)
star = SymbolicCosmology(
    "H0*sqrt(Ωm*(1+z)**3 + ΩΛ + a*z + b*z**2)",
    {"H0": 70, "Ωm": 0.3, "ΩΛ": 0.7, "a": -0.05, "b": 0.01}
)

# 5. Compute χ²
from src.physics.hubble_tension import chi2
chi2_lcdm = chi2(lcdm, z, mu_obs, sigma_mu)
chi2_star = chi2(star, z, mu_obs, sigma_mu)

# 6. Bayesian evidence
logZ_lcdm = log_evidence_laplace(chi2_lcdm, k=2, n=len(z))
logZ_star = log_evidence_laplace(chi2_star, k=4, n=len(z))

B = bayes_factor(logZ_star, logZ_lcdm)
print("Bayes factor:", B)
print("Jeffreys scale:", jeffreys_scale(B))

# 7. Plot comparison
plt.figure(figsize=(10,6))
plt.errorbar(z, mu_obs, sigma_mu, fmt="o", label="Planck")
plt.plot(z, [lcdm.distance_modulus(zi) for zi in z], label="ΛCDM")
plt.plot(z, [star.distance_modulus(zi) for zi in z], label="S.T.A.R.")
plt.legend()
plt.grid()
plt.show()
