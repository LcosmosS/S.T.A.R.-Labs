import pandas as pd
data = pd.read_csv('manga_pipe3d_catalog.csv')
features = ['log_SFR_Ha', 'log_Mass_gas', 'nsa_mstar', 'log_Mass']  # Add your vectors here
df = data[features]
