import importlib, inspect, sys
import acsc.projection as proj_mod
importlib.reload(proj_mod)
from acsc.projection import project as project_records

print("Using projection module:", inspect.getsourcefile(proj_mod))

# re-run projection on your cleaned records
import pandas as pd
rec_df = pd.read_csv("acsc_validation_cremona.csv")  # or the DataFrame you used
records_for_proj = rec_df.to_dict(orient="records")

coords_primary = project_records(records_for_proj, method="primary", Amax=Amax, Nmax=Nmax, V0=V0)
coords_ptd     = project_records(records_for_proj, method="ptd", Amax=Amax, Nmax=Nmax, V0=V0)
coords_mcj     = project_records(records_for_proj, method="mcj", Amax=Amax, Nmax=Nmax, V0=V0)

print("Primary coords shape:", coords_primary.shape)
print("Primary coords sample (first 5):")
print(coords_primary[:5])
