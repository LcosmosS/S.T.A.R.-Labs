import pandas as pd
df = pd.read_csv('Stellar_Mass2_Table.csv')
logmasses = df['logmass']
masses = [10**lm for lm in logmasses if lm != -9999]
with open('masses.gp', 'w') as f:
f.write('masses = ' + str(masses) + ';\n')
