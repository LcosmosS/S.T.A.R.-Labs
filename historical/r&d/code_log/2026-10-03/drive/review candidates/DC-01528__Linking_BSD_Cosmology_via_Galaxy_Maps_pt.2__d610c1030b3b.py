import pandas as pd
df = pd.read_csv('Stellar_Mass2_Table.csv')
valid_df = df[(df['logmass'] != -9999) & (df['z'] != -9999)].head(1000)
log_mass = valid_df['logmass'].tolist()
z = valid_df['z'].tolist()
with open('C:\\temp\\data.gp', 'w') as f:
    f.write('log_mass = [\n')
    for value in log_mass:
        f.write(str(value) + ',\n')
    f.write('];\n')
    f.write('z = [\n')
    for value in z:
        f.write(str(value) + ',\n')
    f.write('];\n')
