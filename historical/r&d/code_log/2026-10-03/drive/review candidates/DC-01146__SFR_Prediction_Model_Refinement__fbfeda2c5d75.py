import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.ensemble import GradientBoostingRegressor
import shap


# --- Step 1: Simulate Galaxy-Like Data ---
np.random.seed(42)
n = 500


df = pd.DataFrame({
    "log_Mass_gas": np.random.normal(9.5, 0.5, n),         # Log gas mass
    "metallicity": np.random.normal(8.6, 0.1, n),          # 12 + log(O/H)
    "dust_attenuation": np.random.normal(1.0, 0.3, n),     # A_V in mag
})


# Synthetic log_SFR target using a physically motivated formula + noise
df["log_SFR"] = (
    0.8 * df["log_Mass_gas"] -
    0.5 * df["metallicity"] +
