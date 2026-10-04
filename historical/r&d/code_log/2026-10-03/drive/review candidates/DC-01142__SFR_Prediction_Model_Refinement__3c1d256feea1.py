import numpy as np
import pandas as pd
from sklearn.ensemble import GradientBoostingRegressor
import shap
import matplotlib.pyplot as plt


# --- Generate simulated galaxy-like dataset ---
np.random.seed(42)
n = 500


df = pd.DataFrame({
    "log_Mass_gas": np.random.normal(9.5, 0.5, n),         # Log of gas mass
    "metallicity": np.random.normal(8.6, 0.1, n),          # 12 + log(O/H)
    "dust_attenuation": np.random.normal(1.0, 0.3, n),     # A_V in magnitudes
})


# --- Create a synthetic SFR function ---
df["log_SFR"] = (
    0.8 * df["log_Mass_gas"]           # strong positive
    - 0.5 * df["metallicity"]          # mild negative
