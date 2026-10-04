import pandas as pd
df = pd.read_csv("synthetic_cosmos_parallel/synthetic_cosmic_catalog.csv")
print(df.groupby('exact_rank')[['V_comove', 'rho_scale', 'betti_1']].mean().round(2))
