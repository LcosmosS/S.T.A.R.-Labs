import pandas as pd
df = pd.read_csv('MyTable_Bigsby.csv')
logmasses = df['log_mass']
valid_logmasses = logmasses[logmasses != -9999]
masses = 10 ** valid_logmasses
M0 = np.median(masses)
sum_M_over_M0 = np.sum(masses / M0)
sum_M0_over_M = np.sum(M0 / masses)
K = sum_M_over_M0 / sum_M0_over_M
print(f"K for MyTable_Bigsby.csv: {K}")
