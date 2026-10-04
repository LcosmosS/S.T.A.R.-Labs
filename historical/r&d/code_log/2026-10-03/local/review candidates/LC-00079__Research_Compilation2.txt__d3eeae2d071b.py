# Save as /home/user/cosmology/preprocess.py
import pandas as pd
df = pd.read_csv('/home/user/cosmology/Stellar_Mass2_Table.csv')
df = df[df['logmass'] != -9999]  # Remove invalid entries
masses = [10**x for x in df['logmass']]  # Convert logmass to mass
with open('/home/user/cosmology/data.gp', 'w') as f:
    f.write(f"masses = {masses};\n")
