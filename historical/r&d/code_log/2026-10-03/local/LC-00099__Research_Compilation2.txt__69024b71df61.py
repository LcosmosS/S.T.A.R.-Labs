# /home/user/cosmology/preprocess.py
import pandas as pd
df = pd.read_csv('/home/user/cosmology/Stellar_Mass2_Table.csv')
df = df[df['logmass'] != -9999]
masses = [10**x for x in df['logmass']]
sfr = df['sfr'].tolist()
with open('/home/user/cosmology/data.gp', 'w') as f:
    f.write(f"masses = {masses};\n")
*     f.write(f"sfr = {sfr};\n")
* Run it again:
* bash
* python3 /home/user/cosmology/preprocess.py
* Weighted L-function in PARI/GP:
* gp
