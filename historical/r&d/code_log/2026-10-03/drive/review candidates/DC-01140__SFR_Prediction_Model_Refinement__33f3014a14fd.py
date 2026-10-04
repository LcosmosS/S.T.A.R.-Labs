import numpy as np
import pandas as pd


np.random.seed(42)
n = 500


df = pd.DataFrame({
    "log_Mass_gas": np.random.normal(9.5, 0.5, n),
    "metallicity": np.random.normal(8.6, 0.1, n),
    "dust_attenuation": np.random.normal(1.0, 0.3, n),
})
df["log_SFR"] = (
    0.8 * df["log_Mass_gas"]
    - 0.5 * df["metallicity"]
