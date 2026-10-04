import pandas as pd
df = pd.read_csv('C:/temp/MyTable_Bigsby.csv')
logmasses = df['log_mass']  # Adjust column name if different, e.g., 'logmass'
valid_logmasses = logmasses[logmasses != -9999]
masses = 10 ** valid_logmasses
with open('C:/temp/masses.txt', 'w') as f:
    for m in masses:
        f.write(str(m) + '\n')
