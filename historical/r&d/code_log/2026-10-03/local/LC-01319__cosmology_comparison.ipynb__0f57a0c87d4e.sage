# 1. Imports
import sys
import os
from pathlib import Path


def get_project_root():
    if "__file__" not in globals():
        cwd = Path(os.getcwd()).resolve()
        for parent in [cwd] + list(cwd.parents):
            if (parent / "src").exists():
                return parent
        return cwd
    return Path(__file__).resolve().parents[1]


ROOT = get_project_root()
sys.path.insert(0, str(ROOT))
print("Project root added to sys.path:", ROOT)

import numpy as np
import matplotlib.pyplot as plt

from src.physics.cosmology import Cosmology
from src.physics.symbolic_cosmology import SymbolicCosmology

# 2. Define ΛCDM
lcdm = Cosmology("H0*sqrt(Ωm*(1+z)**3 + ΩΛ)", {"H0": 70, "Ωm": 0.3, "ΩΛ": 0.7})

# 3. Define S.T.A.R. Model (example symbolic regression output)
star = SymbolicCosmology(
    "H0*sqrt(Ωm*(1+z)**3 + ΩΛ + a*z + b*z**2)",
    {"H0": 70, "Ωm": 0.3, "ΩΛ": 0.7, "a": 0.02, "b": 0.01},
)

# 4. Compute distances
z = np.linspace(0.0, 2.0, 200)
try:
    mu_lcdm = lcdm.distance_modulus(z)
    mu_star = star.distance_modulus(z)
except Exception:
    # Fallback to safe elementwise evaluation (handles functions that only accept scalars)
    mu_lcdm = np.array([lcdm.distance_modulus(float(zi)) for zi in z])
    mu_star = np.array([star.distance_modulus(float(zi)) for zi in z])

# 5. Plot comparison
plt.figure(figsize=(10, 6))
plt.plot(z, mu_lcdm, label="ΛCDM", lw=2)
plt.plot(z, mu_star, label="S.T.A.R. Model", lw=2)
plt.xlabel("Redshift z")
plt.ylabel("Distance Modulus μ")
plt.legend()
plt.title("Distance Modulus Comparison: ΛCDM vs S.T.A.R.")
plt.grid()
# In interactive sessions use plt.show(); in CI use plt.savefig("figure.png")
plt.savefig("figure.png")