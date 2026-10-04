import importlib, inspect
import acsc.alt_mappings as alt
import acsc.projection as proj  # your existing projection
importlib.reload(alt)
importlib.reload(proj)
from acsc.alt_mappings import map_ptd, map_mcj
import pandas as pd, numpy as np

rec_df = pd.read_csv("acsc_validation_cremona.csv")
records = rec_df.to_dict(orient="records")

# choose scaling params consistent with your pipeline
Amax = float(globals().get("Amax", 1.0))
Nmax = float(globals().get("Nmax", 1.0))
V0   = float(globals().get("V0", 1.0))

coords_ptd = map_ptd(records, Amax=Amax, Nmax=Nmax, V0=V0)
coords_mcj = map_mcj(records, Amax=Amax, Nmax=Nmax, V0=V0)

print("PTD coords shape:", coords_ptd.shape)
print("MCJ coords shape:", coords_mcj.shape)
print("PTD sample (first 5):\n", coords_ptd[:5])
print("MCJ sample (first 5):\n", coords_mcj[:5])
