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

from src.physics.cosmology import Cosmology
from src.physics.symbolic_cosmology import SymbolicCosmology

# 2. Define ΛCDM
lcdm = Cosmology(
    "H0*sqrt(Ωm*(1+z)**3 + ΩΛ)",
    {"H0": 70, "Ωm": 0.3, "ΩΛ": 0.7}
)

# 3. Define S.T.A.R. Model (example symbolic regression output)
star = SymbolicCosmology(
    "H0*sqrt(Ωm*(1+z)**3 + ΩΛ + a*z + b*z**2)",
    {"H0": 70, "Ωm": 0.3, "ΩΛ": 0.7, "a": -0.05, "b": 0.01}
)

# 4. Compute distances
z = np.linspace(0, 2, 200)
mu_lcdm = np.array([lcdm.distance_modulus(zi) for zi in z])
mu_star = np.array([star.distance_modulus(zi) for zi in z])

# 5. Plot comparison
plt.figure(figsize=(10,6))
plt.plot(z, mu_lcdm, label="ΛCDM", lw=2)
plt.plot(z, mu_star, label="S.T.A.R. Model", lw=2)
plt.xlabel("Redshift z")
plt.ylabel("Distance Modulus μ")
plt.legend()
plt.title("Distance Modulus Comparison: ΛCDM vs S.T.A.R.")
plt.grid()
plt.show()
