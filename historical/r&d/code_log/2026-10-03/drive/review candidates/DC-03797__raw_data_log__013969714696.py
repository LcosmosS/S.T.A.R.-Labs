import pandas as pd
df = pd.read_csv("synthetic_cosmos_final/synthetic_cosmic_catalog_final.csv")
print(df.groupby('exact_rank')[['V_comove', 'rho_scale', 'betti_1']].mean().round(2))
