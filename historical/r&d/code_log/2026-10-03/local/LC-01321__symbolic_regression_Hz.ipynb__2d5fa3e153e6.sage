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
import pandas as pd
import matplotlib.pyplot as plt

from pysr import PySRRegressor
from src.data.load_sky_surveys import load_sky_surveys
from src.physics.cosmology import Cosmology
from src.physics.symbolic_cosmology import SymbolicCosmology

# 2. Load data
df1, df2 = load_sky_surveys()
df = pd.concat([df1, df2], ignore_index=True)
z = df["redshift"].values
mu_obs = df["mu_obs"].values

# 3. Convert μ → DL → H(z) target
# DL = 10^((μ/5)+1) pc
DL_pc = 10 ** ((mu_obs / 5) + 1)
DL_Mpc = DL_pc / 1e6

# Approximate H(z) target using derivative of DL
# H(z) ≈ c / (dDL/dz / (1+z) - DL/(1+z)^2)
c = 299792.458
dDL_dz = np.gradient(DL_Mpc, z)
H_target = c / (dDL_dz / (1 + z) - DL_Mpc / (1 + z) ** 2)

# 4. Train symbolic regression model
model = PySRRegressor(
    niterations=200,
    unary_operators=["exp", "log"],
    binary_operators=["+", "-", "*", "/", "pow"],
    loss="loss(x, y) = (x - y)^2",
)
model.fit(z.reshape(-1, 1), H_target)

print(model)

# 5. Convert symbolic model to cosmology engine
H_expr = str(model.sympy())
params = {"H0": 70}  # add any constants needed

star = SymbolicCosmology(H_expr, params)

# 6. Compare with ΛCDM
lcdm = Cosmology("H0*sqrt(Ωm*(1+z)**3 + ΩΛ)", {"H0": 70, "Ωm": 0.3, "ΩΛ": 0.7})

# 7. Plot H(z)
z_plot = np.linspace(0, 2, 200)
H_lcdm = [lcdm.H_of_z(zi) for zi in z_plot]
H_star = [star.H(zi) for zi in z_plot]

plt.plot(z_plot, H_lcdm, label="ΛCDM")
plt.plot(z_plot, H_star, label="Symbolic S.T.A.R.")
plt.legend()
plt.show()