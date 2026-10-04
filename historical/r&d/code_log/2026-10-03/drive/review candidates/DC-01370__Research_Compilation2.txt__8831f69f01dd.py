import pandas as pd
import numpy as np
df = pd.read_csv('Stellar_Mass2_Table.csv')
df = df[df['logmass'] != -9999]
masses = 10 ** df['logmass']
N = len(masses)
M0 = np.median(masses)
sum_M_over_M0 = np.sum(masses / M0)
sum_M0_over_M = np.sum(M0 / masses)
K = sum_M_over_M0 / sum_M0_over_M
print(f"K for Stellar_Mass2_Table.csv: {K}")
